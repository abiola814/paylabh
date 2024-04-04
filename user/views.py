from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from .custom_auth import CustomAuthBackend
from .models import User,EmailVerifyTable,PhoneVerifyTable,BenefitaryTable
from .utils import log_request,send_password_reset_mail,send_activation_mail,send_activation_phone,validatingPassword,checkRequest,errorResponse,successResponse,send_welcome_mail
import uuid
from .jwt_token import create_jwt_for_user
from user_agents import parse
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from random import randrange
from django.db.models.query_utils import Q
from .serializer import UserSerializer,UpdateProfileSerializer,TagSerializerIn
from datetime import datetime
from wallet.models import Transaction
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
        code = data.get("referral","")
        verify_phone = User.objects.filter(phone=phone).exists()
        verify_email = User.objects.filter(email=email).exists()
        if verify_email :
            return errorResponse(id,"Sorry , email has been used")
        check_email = EmailVerifyTable.objects.filter(email=email,is_verified=True).exists()
        if not check_email:
            return successResponse(id,"sorry, email is not verified")
        check_phone = PhoneVerifyTable.objects.filter(phone=phone,is_verified=True).exists()
        # if not check_phone:
        #     return successResponse(id,"sorry, phone number is not verified")
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

        referrer=User.objects.filter(referral_code= code).exists()
        if referrer:
            referrer_user=User.objects.get(referral_code=code)
            referrer_user.number_of_referral += 1
            referrer_user.point +=10
            referrer_user.save()
            Transaction.objects.create(user=referrer_user,name=f"{referrer_user.last_name} {referrer_user.first_name}",transaction_type="point credit",transaction_id= (uuid.uuid4())[:12],reference_id= (uuid.uuid4())[:12],status="Success",description=f"point credit from referral from {user.last_name}",remainbalance=referrer_user.point,amount=10)
        user = CustomAuthBackend.authenticate(self,request,credential=email,password=password)
        if user is not None:
            print(user)
            print(user.is_active)
            print(user.active)
            if user.active==False:
                return errorResponse(id,"Your account is not activated")
            tokens = create_jwt_for_user(user)
            send_welcome_mail(user)
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
            if not verify.is_expired():
                verify.is_verified = True
                verify.code=None
                verify.save()
                return successResponse(id,f"{verify.email} verified")
            else:
                return errorResponse(id,"Code expired")
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

class LoginView(generics.GenericAPIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        
        
        password = data.get("password")
        credential = data.get('credential')

        user = CustomAuthBackend.authenticate(self,request,credential=credential,password=password)
        if user is not None:
            print(user)
            print(user.is_active)
            print(user.active)
            if user.active==False:
                return errorResponse(id,"Your account is not activated")
            tokens = create_jwt_for_user(user)
            return successResponse(id,"login successfull","token",tokens)
        return errorResponse(id,"invalid credential")

class PasscodeLoginView(generics.GenericAPIView):

    permission_classes=[]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        
        
        passcode = data.get("passcode")

        user = CustomAuthBackend.authenticatePasscode(self,request,credential=passcode)
        if user is not None:
            print(user)
            print(user.is_active)
            print(user.active)
            if user.active==False:
                return errorResponse(id,"Your account is not activated")
            tokens = create_jwt_for_user(user)
            return successResponse(id,"login successfull","token",tokens)
        return errorResponse(id,"invalid credential")

class CreatePasscodeView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        code = data.get("code")
        user = User.objects.get(id= request.user.id)
        user.passcode=code
        user.save()
        return successResponse(id,"Passcode successfully created")

class CountryView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        country_origin = data.get("country")
        user = User.objects.get(id= request.user.id)
        user.country_origin=country_origin
        user.save()
        return successResponse(id,"country added")

class JoinreasonView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        join_reason = data.get("join_reason")
        user = User.objects.get(id= request.user.id)
        user.join_reason=join_reason
        user.save()
        return successResponse(id,"reason added")

class TagView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        tag_name = data.get("tag_name")
        user = User.objects.get(id= request.user.id)
        if User.objects.filter(tag=tag_name).exists():
            return errorResponse(id,"tag name already used")
        user.tag=tag_name
        user.save()
        return successResponse(id,"tag added")

    def get(self,request:Request):
        search = request.GET.get("search",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        result={"tag":f"{request.user.tag}@LabTag"}
        if search:
           filters = User.objects.filter(tag__icontains=search)
           result = TagSerializerIn(filters, many=True, context={"request": request}).data
        
        return successResponse(id,"tag","tag",result) 
    def put(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        tag_name = data.get("tag_name")
        user = User.objects.get(id= request.user.id)
        if User.objects.filter(tag=tag_name).exists():
            return errorResponse(id,"tag name already used")
        user.tag=tag_name
        user.save()
        return successResponse(id,"tag updates")
    

class TransactionPinView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        pin = data.get("pin")
        user = User.objects.get(id= request.user.id)
        user.transaction_pin=pin
        user.is_Pin=True
        user.save()
        return successResponse(id,"Transaction Pin successfully created")
    def put(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        pin = data.get("pin")
        newpin = data.get("newpin")
        user = User.objects.get(id= request.user.id)
        if int(pin) == user.transaction_pin :
            user.transaction_pin=newpin
            user.save()
            return successResponse(id,"Transaction pin successfully updated")
        else:
            return errorResponse(id,"old transaction pin not correct")




class ProfileImage(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request:Request):
        image = request.data.get('image')
        
        id = uuid.uuid4()
        id = str(id)[:8]
        log_request(f"referenceId:{id},{image}")
        user = User.objects.get(id=request.user.id)
        if not image:
            return errorResponse(id,"unable to update image please check the image selected")
        user.avatar=image
        user.save()
        return successResponse(id,"profile image added")


#forgot password 
class ForgotPasswordView(generics.GenericAPIView):
    
    permission_classes=[]
    def post(self,request:Request):
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        if checkRequest(id,data=data):
            return checkRequest(id,data=data)
        email= data.get("email")
        if email:
            #check if email exist in the database
            associated_users = User.objects.filter(Q(email=email))
            # send email to user if the email exist
            return send_password_reset_mail(id,associated_users)
        else:
            return errorResponse(id,"Email is required")
    def put(self,request:Request):

        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        checkRequest(id,data)
        new= data.get("newpassword")
        confirm= data.get("confirmpassword")
        code= data.get("code")
        if new is None:
            return errorResponse(id,"new password is required")
        if code is None:
 
            return errorResponse(id,"code is required")
        if confirm is None:
            return errorResponse(id,"Confirm password is required")
        if confirm != new:
            return errorResponse(id,"confirm password and new password do not matched")
        check_code = User.objects.filter(recoveryCode=code)
        print(check_code)
        if not check_code.exists():
            return errorResponse(id,"Sorry your code is invalid")
        user = User.objects.get(recoveryCode=code)
        user.set_password(confirm)
        user.recoveryCode=None
        user.save()
        return successResponse(id,f"Password successfully changed for {user.last_name}",None,None)


#change password for user
class Changepassword(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def patch(self,request:Request):
        data=request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        log_request(f"referenceId:{id},{data}")
        old_password = data.get("oldPassword")
        new_password = data.get("newPassword")
        confirm_password = data.get("confirmPassword")
        if old_password is None:
            return errorResponse(id,"Please , input your old password")
        if new_password is None:
            return errorResponse(id,"Please , input your new password")
        if confirm_password is None:
            return errorResponse(id,"Please , input your confirm password")
        if confirm_password != new_password:
            return errorResponse(id,"Sorry , your confirm password and new password did not match")
        user = User.objects.get(id=request.user.id)
        checkPassword =user.check_password(old_password)
        if not checkPassword:
            return errorResponse(id,"Sorry , incorrect old password")
        else:
            user.set_password(confirm_password)
            user.save()        
            return successResponse(id,"Password changed successfully")

class Profile(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        id = uuid.uuid4()
        id = str(id)[:8]
        log_request(f"referenceId:{id}")
        # serializer to handle turning our `Profile` object into something that 
        # can be JSONified and sent to the client. 
        serializer = self.serializer_class(request.user,context={"request":request})
        
        return successResponse(id,"successfully proccessed","user",serializer.data)
    def put(self, request, *args, **kwargs):
        # username = request.data.get("username",False)
        # phone = request.data.get("phone",False)
        # name= request.data.get("name",False)
        # email= request.data.get("email",False)
        
        # temp_data = {'username':username,"phone":phone,"name":name,"email":email} 
        data = request.data.get("data",None)
        id = uuid.uuid4()
        id = str(id)[:8]
        log_request(f"referenceId:{id},{data}")
        if data is None:
            response ={ 'requestTime':datetime.now(),'referenceId':id,"requestType":"outbound",
            "message":"Please , add your data json",
            "status":False,
            }
            log_request(f"{response}")
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        serializer_data=request.data.get("data")
        serializer = UpdateProfileSerializer(
            request.user, data=serializer_data, partial=True
        )
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return successResponse(id,"Profile successfully updated","user",serializer.data)
        else:
            serializer.save()
            response ={  'requestTime':datetime.now(),'referenceId':id, "requestType":"outbound",
                            "message": "Unable to update your profile",
                            "status":True,
                            "data":{
                                    "user": serializer.errors
                            }
                            }
            log_request(f"{response}")
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)



class ReferralLinkView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        id = uuid.uuid4()
        id = str(id)[:8]
        log_request(f"referenceId:{id}")
        user = request.user

        referral_code = user.referral_code

        custom_url_scheme = 'myapp://'  # Replace 'myapp://' with your actual app's custom URL scheme
        referral_link = f"{custom_url_scheme}referral/{referral_code}"

        user_agent = parse(request.META['HTTP_USER_AGENT'])

        if user_agent.is_mobile:
            if user_agent.is_ios:
                # Redirect to the custom URL scheme for iOS
                redirect_url = referral_link
            elif user_agent.is_android:
                # Redirect to the custom URL scheme for Android
                redirect_url = referral_link
            else:
                # Redirect to the app store URL if the device is not iOS or Android
                app_store_url = 'https://example.com/appstore-link/'  # Replace with the actual app store URL
                return successResponse(id,"referral link","referral",app_store_url)
        else:
            # Redirect to the app store URL if the user is not on a mobile device
            app_store_url = 'https://example.com/appstore-link/'  # Replace with the actual app store URL
            return successResponse(id,"referral link","referral",referral_link)

        return successResponse(id,"referral link","referral",referral_link)



class Beneficairy(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        id = uuid.uuid4()
        id = str(id)[:8]
        log_request(f"referenceId:{id}")
        allrecord = BenefitaryTable.objects.filter(saveUser=request.user).values()
        return successResponse(id,"done","beneficiary",allrecord)
