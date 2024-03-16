from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import re

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        UserModel = get_user_model()
        try:
            data = kwargs.get('credential', None)
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if(re.fullmatch(regex, data)):
                user = UserModel.objects.get(email=data)
            # print("lllllllllllllllllllllll")
            else:
                user = UserModel.objects.get(phone=data)
            if user.check_password(kwargs.get('password', None)):
                return user
        except UserModel.DoesNotExist:
            return None
        return None
    def authenticatePasscode(self, request, **kwargs):
        UserModel = get_user_model()
        try:
            data = kwargs.get('credential', None)
            user = UserModel.objects.get(passcode=data)
        except UserModel.DoesNotExist:
            return None
        return None
        
        
    
        
        

