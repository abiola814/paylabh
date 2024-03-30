from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from random import randrange

class UserSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()

    def get_tag(self,obj):
        return f"{obj.tag}@LabTag"

    class Meta(object):
        model = User
        fields = ('id', 'first_name','last_name','first_login','verified',"is_bvn",'email','phone',"avatar","tag","country_origin",
                  )
class TagSerializerIn(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()

    def get_tag(self,obj):
        return f"{obj.tag}@LabTag"

    class Meta(object):
        model = User
        fields = ('tag', 'first_name','last_name'
                  )

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ("email","country_origin")
