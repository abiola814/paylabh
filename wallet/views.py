from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from user.models import User
from user.utils import log_request,send_password_reset_mail,send_activation_mail,send_activation_phone,validatingPassword,checkRequest,errorResponse,successResponse
import uuid
# from .providus import create_naira_account
from .coralpay import createNairaAccount,check_user_bank_details,bank_transfer
from .models import Transaction,Wallet,Vault,Duration
from .serializer import TransactionSerializer,WalletSerializer,DurationSerializer,VaultSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models.query_utils import Q
from django.conf import settings
from .utils import labtransfer
from billPayment.bills import walletProcess
# Create your views here.
class TransactionsView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        transid= data.get("id")
        trans = Transaction.objects.filter(id=transid)
        serializer_data=TransactionSerializer(trans, context={"request": request},many=True)
          
        return successResponse(id,"all transactions","transaction",serializer_data.data)
    def get(self,request:Request):
        id = uuid.uuid4()
        id = str(id)[:8]
        trans = Transaction.objects.all()
        serializer_data=TransactionSerializer(trans, context={"request": request},many=True)
          
        return successResponse(id,"all transactions","transaction",serializer_data.data)

class WalletView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        transid= data.get("currency")
        trans = Wallet.objects.filter(currency_code=transid)
        serializer_data=WalletSerializer(trans, context={"request": request},many=True)
          
        return successResponse(id,"all transactions","transaction",serializer_data.data)
    def get(self,request:Request):
        id = uuid.uuid4()
        id = str(id)[:8]
        user = User.objects.get(id=request.user.id)
        wallet = Wallet.objects.filter(user=user)
        serializer_data=WalletSerializer(wallet, context={"request": request},many=True)
        return successResponse(id,"all wallets","wallets",serializer_data.data)

class VaultView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self, request, format=None):
        id = uuid.uuid4()
        id = str(id)[:8]
        data =request.data["data"]
        data["user"]=request.user.id
        serializer = VaultSerializer(data=data)
        if serializer.is_valid():
            vault = serializer.save()
            return successResponse(id,'Vault created successfully.',"vault",serializer.data)
        return errorResponse(id,serializer.errors)
    def get(self,request:Request):
        id = uuid.uuid4()
        id = str(id)[:8]
        vault_type = request.GET.get('vault_type')
        
        if vault_type == 'safe':
            vaults = Vault.objects.filter(vault_type='safe',user=request.user.id)
        elif vault_type == 'target':
            vaults = Vault.objects.filter(vault_type='target',user=request.user.id)
        else:
            vaults = Vault.objects.filter(user=request.user.id)
        

        serializer_data=VaultSerializer(vaults, context={"request": request},many=True)
          
        return successResponse(id,"all vault","vault",serializer_data.data)
    def put(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)
        try:
            vault= Vault.objects.get(id=data.get("id"))
        except Exception as e:
            return errorResponse(id,str(e))
        serializer_data=VaultSerializer(instance=vault,data=data,context={"request": request},partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
        else:
            return errorResponse(id,serializer_data.errors)
        return successResponse(id,"updated","vault",serializer_data.data)
    def delete(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)
        
        try:
            instance = Vault.objects.get(id=data.get("id"))
            instance.delete()
        
        except Vault.DoesNotExist:
            return errorResponse(id,'vault does not exist')
        except Exception as e:
            return errorResponse(id,str(e))
        return successResponse(id,"vault deleted")

class AccountView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)
        user = User.objects.get(id=request.user.id)
        currency = data.get("currency")
        if Wallet.objects.filter(user=user,currency_code__iexact=currency).exists():
            return errorResponse(id,"you cannot create double naira account")
        if currency == 'NGN':
            status,account_name,account_number,bank_name= createNairaAccount(user)
            if status != "00":
                return errorResponse(id,"unable to create naira account")
        else:
            return errorResponse(id,f"currency {currency} is not available")
        data={
            "user":user.id,
            "account_name":account_name,
            "account_number":account_number,
            "currency_code":currency,
            "bank_name":bank_name
            
        }
        serializer_data=WalletSerializer(data=data)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
        else:
            return errorResponse(id,serializer_data.errors)
          
        return successResponse(id,"account created","account",serializer_data.data)
    

class LabTransferView(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)
        user = User.objects.get(id=request.user.id)
        currency = data.get("currency")
        amount = data.get("amount")
        tagname = data.get("labtag")
        balance = walletProcess(user=request.user)
        if currency == "NGN":
            trans = Transaction,object.create(user=request.user,name=f"{request.user.last_name} {request.user.first_name}",
                transaction_type="Debit",transaction_id= (uuid.uuid4())[:12],reference_id= (uuid.uuid4())[:12],status="Pending",
                description=f"transfer to  {tagname}",remainbalance=balance,amount=amount)
            info,status=labtransfer(request,amount,tagname,id)
            if status == "failed":
                return errorResponse(id,info)
            else:
                trans.status="success"
                trans.save()
                return successResponse(id,info)
            

class DurationView(APIView):

    permission_classes=[IsAuthenticated]
    def get(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        durate = Duration.objects.all()
        serializer_data = DurationSerializer(durate,many=True)
        return successResponse(id,"all Duration","duration",serializer_data.data)



class PaybackView(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)
        dur = data.get("id")
        duration = Duration.objects.get(id=dur)
        serializer_data = DurationSerializer(dur,many=True)        # Serialize the result into a JSON-serializable format
        date_range_with_increasing_percentage = duration.generate_date_range_with_increasing_percentage()
        import json

        # Serialize to JSON
        result_json = json.dumps(date_range_with_increasing_percentage)
        return successResponse(id,"all Duration","duration",date_range_with_increasing_percentage)


class BankListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        bank = settings.BANK_LIST
        return successResponse(id,"ALL BANK LIST","BANK",bank)


class CheckUserBankDetails(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)
        number = data.get("number")
        bankCode = data.get("bankCode")

        if number and bankCode:
            result = check_user_bank_details(number, bankCode)
            if not result:
                return errorResponse(id,"unable to verify bank details")
            return successResponse(id,"bank details","BANK",result)
            
        else:
            return errorResponse(id,"both account number and code is required")


class BankTransfer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)

        if all(key in data for key in ["accountNumber", "accountName", "bankCode", "narration", "amount"]):
            result = self.bank_transfer(data)
            return  successResponse(id,"amount transferred")
        else:
            return errorResponse(id,'Missing required parameters')
