from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from threading import Thread
from user.models import User,BenefitaryTable
from user.utils import log_request,send_password_reset_mail,send_activation_mail,send_activation_phone,validatingPassword,checkRequest,errorResponse,successResponse
import uuid
from billPayment.permissions import IsWallet
# from .providus import create_naira_account
from .coralpay import createNairaAccount,check_user_bank_details,bank_transfer
from .models import Transaction,Wallet,Vault,Duration
from .serializer import TransactionSerializer,WalletSerializer,DurationSerializer,VaultSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models.query_utils import Q
from django.conf import settings
from .utils import labtransfer,calculate_charge_fee,send_debit_mail,send_credit_mail
from billPayment.bills import walletProcess
from datetime import datetime
# Create your views here.
class TransactionsView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        transid= data.get("id")
        trans = Transaction.objects.filter(user=request.user,id=transid)
        serializer_data=TransactionSerializer(trans, context={"request": request},many=True)
          
        return successResponse(id,"all transactions","transaction",serializer_data.data)
    def get(self,request:Request):
        id = uuid.uuid4()
        id = str(id)[:8]
        trans = Transaction.objects.filter(user=request.user).order_by('-timestamp')
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

    permission_classes=[IsAuthenticated,IsWallet]

    def post(self, request, format=None):
        id = uuid.uuid4()
        id = str(id)[:8]
        data =request.data["data"]
        data["user"]=request.user.id
        if not data.get('pin') == request.user.transaction_pin:
            return errorResponse(id,"Transaction pin not correct")
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
    
class TransferReview(APIView):
    permission_classes=[IsAuthenticated] 
    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)
        amount = data.get("amount")
        balance = walletProcess(user=request.user,type=1,amount=amount,id=id)
        if not balance:
            return errorResponse(id,"insufficient balance")
        charge = calculate_charge_fee("LabTransferFee",int(amount))
        return successResponse(id,"charge calculated","chargeFee",charge)
        


class LabTransferView(APIView):  

    permission_classes=[IsAuthenticated,IsWallet]
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
        pin = data.get("pin",None)
        trans_id=  (str(uuid.uuid4()))[:12]
        ref_id =  (str(uuid.uuid4()))[:12]
        if not pin == request.user.transaction_pin:
            return errorResponse(id,"Transaction pin not correct")
        charge = calculate_charge_fee("LabTransferFee",int(amount))
        balance = walletProcess(user=request.user,type=4,id=id)
        if currency == "NGN":
            total_remove_amount = int(amount) + charge["chargeFee"]
            trans = Transaction.objects.create(user=request.user,name=f"{request.user.last_name} {request.user.first_name}",
                transaction_type="Debit",transaction_id= trans_id,reference_id= ref_id,status="Pending",
                description=f"transfer to  {tagname}",remainbalance=balance,amount=total_remove_amount,is_LabTransfer=True)
            info,status=labtransfer(request,amount,tagname,id,ref_id,trans_id,charge["chargeFee"])
            if status == "failed":
                return errorResponse(id,info)
            elif status =="reverse":
                trans.status="Reverse"
                trans.save()
                walletProcess(user=request.user,type=3,amount=total_remove_amount,id=id)
                return errorResponse(id,info)
            else:
                trans.status="Success"
                trans.save()
                Thread(target=send_debit_mail, args=[request.user.email,info]).start()
                Thread(target=send_credit_mail, args=[info["email"],info]).start()

                return successResponse(id,"money sent","data",info)
        return errorResponse(id,"Currency not supported coming soon")
        
            

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
    permission_classes = [IsAuthenticated,IsWallet]

    def post(self, request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data):
            return checkRequest(id,data)
        pin = data.get("pin",None)
        amount= data.get("amount",None)
        ben = data.get("saved",None)

        trans_id=  (str(uuid.uuid4()))[:12]
        ref_id =  (str(uuid.uuid4()))[:12]
        if not pin == request.user.transaction_pin:
            return errorResponse(id,"Transaction pin not correct")
        charge = calculate_charge_fee("LabTransferFee",int(amount))
        balance = walletProcess(user=request.user,type=4,id=id)
        if all(key in data for key in ["accountNumber", "accountName", "bankCode", "narration", "amount"]):
            total_remove_amount = int(amount) + charge["chargeFee"]
            trans = Transaction.objects.create(user=request.user,name=f"{request.user.last_name} {request.user.first_name}",
            transaction_type="Debit",transaction_id= trans_id,reference_id= ref_id,status="Pending",
            description=data.get("narration"),remainbalance=balance,amount=total_remove_amount,is_Transfer=True,DestinationAccountNumber=data.get("accountNumber"),DestinationAccountName=data.get("accountName"),DestinationBankName=data.get("bankCode"))
            result,status = bank_transfer(user=request.user,data=data,charge=charge["chargeFee"])
            if status == "failed":
                return errorResponse(id,result)
            elif status =="reverse":
                trans.status="Reverse"
                trans.save()
                walletProcess(user=request.user,type=3,amount=total_remove_amount,id=id)
                return errorResponse(id,result)
            else:
                trans.response=result
                trans.reference_id=result["traceId"]
                trans.save()
            if not ben:
                BenefitaryTable.objects.create(accountName=data["accountNumber"],accountNumber=data["accountName"],bankCode=data["bankCode"],saveUser=request.user)
                # Thread(target=send_debit_mail, args=[request.user.email,{"sender":f"{request.user.first_name} {request.user.last_name}","time":datetime.now(),"transId":trans_id,"amount":amount}]).start()
            return  successResponse(id,"amount transferred","data",{"sender":f"{request.user.first_name} {request.user.last_name}","time":datetime.now(),"transId":trans_id,"amount":amount,"chargeFee":charge["chargeFee"]})
        else:
            return errorResponse(id,'Missing required parameters')
