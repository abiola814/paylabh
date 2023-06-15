from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from .custom_auth import CustomAuthBackend
from .models import User,EmailVerifyTable,PhoneVerifyTable
from .utils import log_request,send_activation_mail,send_activation_phone,validatingPassword,checkRequest,errorResponse,successResponse
import uuid
from .jwt_token import create_jwt_for_user
from rest_framework.permissions import IsAuthenticated


# Create your views here.
"""
this api view is responsible for the signing up of user base on some parameter

"""
class SignupView(generics.GenericAPIView):

    permission_classes=[]
    """
    post request
    request: {phonenumber:int , email:string ,password:string ,username:sting}
    response: {
        'requestTime':datetime,
        'referenceId':string,
        "requestType":string,
        "message": string,
        "status":bool
    }
    """
    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        
        
        password = data.get("password")
        email = data.get('email')

        phone = data.get('phone')
        first = data.get('first')
        last = data.get('last')
        verify_phone = User.objects.filter(phone=phone).exists()
        verify_email = User.objects.filter(email=email).exists()
        if verify_email :
            return errorResponse(id,"Sorry , email has been used")
        check_email = EmailVerifyTable.objects.filter(email=email,is_verified=True).exists()
        if not check_email:
            return successResponse(id,"sorry, email is not verified")
        check_phone = PhoneVerifyTable.objects.filter(phone=phone,is_verified=True).exists()
        if not check_phone:
            return successResponse(id,"sorry, phone number is not verified")
        if verify_phone:
            return errorResponse(id,"sorry, phone number has been used")
        result = validatingPassword(password)
        if result is not True:
            print(result)
            return errorResponse(id,result)

        try:      
            User.objects.create_user(email=email,phone=phone,password=password,last_name=last,first_name=first)

        except ValueError as error:
            log_request(f"{error}")
            return errorResponse(id,str(error))

        user = CustomAuthBackend.authenticate(self,request,credential=email,password=password)
        if user is not None:
            print(user)
            print(user.is_active)
            print(user.active)
            if user.active==False:
                return errorResponse(id,"Your account is not activated")
            tokens = create_jwt_for_user(user)
            return successResponse(id,"login successfull","token",tokens)
        return successResponse(id,"Account successfully created")
        
        # return Response(data=response,status=status.HTTP_201_CREATED)

class verifyMail(generics.GenericAPIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        email = data.get('email')
        verify_email = User.objects.filter(email=email).exists()

        if verify_email :
            return errorResponse(id,f"Sorry , {email} has been used")
        return successResponse(id,f"{email} has not been used")

class activateMail(generics.GenericAPIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        email = data.get('email')
        return send_activation_mail(id,email)

class verifyPhone(generics.GenericAPIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        phone = data.get('phone')
        verify_phone = User.objects.filter(phone=phone).exists()

        if verify_phone :
            return errorResponse(id,f"Sorry , {phone} has been used")
        return successResponse(id,f"{phone} has not been used")
class activatePhone(generics.GenericAPIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        phone = data.get('phone')
        return send_activation_phone(id,phone)

class EmailVerifycode(generics.GenericAPIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        code = data.get('code')
        checking= EmailVerifyTable.objects.filter(code=code)
        if checking.exists():
            verify = EmailVerifyTable.objects.get(code=code)
            verify.is_verified = True
            verify.code=None
            verify.save()
            return successResponse(id,f"{verify.email} verified")
        else:
            return errorResponse(id,"wrong code")

class PhoneVerifycode(generics.GenericAPIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        code = data.get('code')
        checking= PhoneVerifyTable.objects.filter(code=code)
        # if checking.exists():
        for i in checking:
            verify = PhoneVerifyTable.objects.get(phone=i.phone)
            verify.is_verified = True
            verify.save()
            return successResponse(id,f"{verify.phone} verified")
        # else:
        #     return errorResponse(id,"wrong code")

