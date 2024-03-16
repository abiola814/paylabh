from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from random import randrange

class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'first_name','last_name','first_login','verified',"is_bvn",'email','phone',"avatar","tag","country_origin",
                  )


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ("email","country_origin")