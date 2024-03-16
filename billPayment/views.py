from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from user.models import User,EmailVerifyTable,PhoneVerifyTable
from user.utils import log_request,send_password_reset_mail,send_activation_mail,send_activation_phone,validatingPassword,checkRequest,errorResponse,successResponse
import uuid
from .models import DataBundle,NetworkType,Bills,Cable,Exam
from .serializer import DataBundleSerializer,NetworkSerializer,CableSerializer,ExamSerializer,BillsSerializer
from .bills import buy_data,buy_airtime,buy_bills,confirm_coralpay,buy_coralpay,all_bet,coral_check,buy_result,all_electric,all_cable
from rest_framework.permissions import IsAuthenticated
from django.db.models.query_utils import Q
from .utils import check_transaction_pin
from random import randrange

# Create your views here.
class Databundle(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        transaction_pin = data.get("transaction_pin")
        user = User.objects.get(id= request.user.id)
        if not transaction_pin:
            return errorResponse(id, "Transaction pin is required.")

        # Check if the provided transaction pin is correct
        if not check_transaction_pin(user, transaction_pin):
            return errorResponse(id, "Invalid transaction pin.")
        info,status=buy_data(data.get("network"),data.get("dataplan"),data.get("number"),data.get("amount"),id,request,id)
        if status == "failed":
            return errorResponse(id,info)
        else:
            return successResponse(id,info)
    def get(self,request:Request):
        id = uuid.uuid4()
        id = str(id)[:8]
        databundle={}
        networks = NetworkType.objects.all()
        for network in networks:
            network_sel = DataBundle.objects.filter(networkType=network)
            serializer_data=DataBundleSerializer(network_sel, context={"request": request},many=True)
            info = {network.network:serializer_data.data}
            databundle.update(info)
        return successResponse(id,"all data plan","DataPlan",databundle)

class Airtime(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        transaction_pin = data.get("transaction_pin")
        if not transaction_pin:
            return errorResponse(id, "Transaction pin is required.")

        # Check if the provided transaction pin is correct
        user = User.objects.get(id= request.user.id)
        if not check_transaction_pin(user, transaction_pin):
            return errorResponse(id, "Invalid transaction pin.")
        code = data.get("code")
        info,status=buy_airtime(request,data.get("network"),data.get("number"),data.get("amount"),id,id)
        if status == "failed":
            return errorResponse(id,info)
        else:
            return successResponse(id,info)
    def get(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        databundle=[]
        networks = NetworkType.objects.all()
        serializer_data=NetworkSerializer(networks, context={"request": request},many=True)
  
        return successResponse(id,"all airtime network","network",serializer_data.data)


class Electricity(APIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        status = data.get("status")
        if status == "confirm":
            result,stats = confirm_coralpay(data.get("customer_number"),data.get("biller_slug"),data.get("productName"))
            if stats == "failed":
                return errorResponse(id,result)
            return successResponse(id,"proccesed","result",result)
        transaction_pin = data.get("transaction_pin")
        if not transaction_pin:
            return errorResponse(id, "Transaction pin is required.")

        # Check if the provided transaction pin is correct
        if not check_transaction_pin(request.user, transaction_pin):
            return errorResponse(id, "Invalid transaction pin.")
        paymentref=randrange(1000000000000,9999999999999)
        info,status=buy_coralpay(request,data.get("customer_number"),paymentref,data.get("productName"), data.get("amount"),id)
        if status == "failed":
            return errorResponse(id,info)
        else:
            return successResponse(id,info)
    def get(self,request:Request,status=None,billerslug=None):
        
        id = uuid.uuid4()
        id = str(id)[:8]
        print("nhhhghgg")
        status = request.GET.get("status")
        slug = request.GET.get("billerslug")
        print(slug,status)
        if status != "all":
            result,stats = coral_check(slug)
            if stats == "failed":
                return errorResponse(id,result)
        else:
            result,stats = all_electric()
            if stats == "failed":
                return errorResponse(id,result)

  
        return successResponse(id,"all electricity","electric",result)

class CableView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        status = data.get("status")
        if status == "confirm":
            result,stats = confirm_coralpay(data.get("customer_number"),data.get("biller_slug"),data.get("productName"))
            if stats == "failed":
                return errorResponse(id,result)
            return successResponse(id,"proccesed","result",result)
        transaction_pin = data.get("transaction_pin")
        if not transaction_pin:
            return errorResponse(id, "Transaction pin is required.")

        # Check if the provided transaction pin is correct
        if not check_transaction_pin(request.user, transaction_pin):
            return errorResponse(id, "Invalid transaction pin.")
        paymentref=randrange(1000000000000,9999999999999)
        info,status=buy_coralpay(request,data.get("customer_number"),paymentref,data.get("productName"), data.get("amount"),id)
        if status == "failed":
            return errorResponse(id,info)
        else:
            return successResponse(id,info)
    def get(self,request:Request,status=None,billerslug=None):
        
        id = uuid.uuid4()
        id = str(id)[:8]
        print("nhhhghgg")
        status = request.GET.get("status")
        slug = request.GET.get("billerslug")
        print(slug,status)
        if status != "all":
            result,stats = coral_check(slug)
            if stats == "failed":
                return errorResponse(id,result)
        else:
            result,stats = all_cable()
            if stats == "failed":
                return errorResponse(id,result)

  
        return successResponse(id,"all cables","cable",result)

class ResultView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        transaction_pin = data.get("transaction_pin")
        if not transaction_pin:
            return errorResponse(id, "Transaction pin is required.")

        # Check if the provided transaction pin is correct
        if not check_transaction_pin(user, transaction_pin):
            return errorResponse(id, "Invalid transaction pin.")
        info,status=buy_result(request,data.get("exam"),data.get("quantity"),data.get("amount"),id,id)
        if status == "failed":
            return errorResponse(id,info)
        else:
            return successResponse(id,info)
    def get(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        result = Exam.objects.all()
        serializer_data=ExamSerializer(result, context={"request": request},many=True)
  
        return successResponse(id,"all exam names","exams",serializer_data.data)





class BetView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        status = data.get("status")
        if status == "confirm":
            result,stats = confirm_coralpay(data.get("customer_number"),data.get("biller_slug"),data.get("productName"))
            if stats == "failed":
                return errorResponse(id,result)
            return successResponse(id,"proccesed","result",result)
        transaction_pin = data.get("transaction_pin")
        if not transaction_pin:
            return errorResponse(id, "Transaction pin is required.")

        # Check if the provided transaction pin is correct
        if not check_transaction_pin(request.user, transaction_pin):
            return errorResponse(id, "Invalid transaction pin.")
        paymentref=randrange(1000000000000,9999999999999)
        info,status=buy_coralpay(request,data.get("customer_number"),paymentref,data.get("productName"), data.get("amount"),id)
        if status == "failed":
            return errorResponse(id,info)
        else:
            return successResponse(id,info)
    def get(self,request:Request,status=None,billerslug=None):
        
        id = uuid.uuid4()
        id = str(id)[:8]
        print("nhhhghgg")
        status = request.GET.get("status")
        slug = request.GET.get("billerslug")
        print(slug,status)
        if status != "all":
            result,stats = coral_check(slug)
            if stats == "failed":
                return errorResponse(id,result)
        else:
            result,stats = all_bet()
            if stats == "failed":
                return errorResponse(id,result)

  
        return successResponse(id,"all bet","bet",result)
