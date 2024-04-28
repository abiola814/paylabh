# serializers.py
from rest_framework import serializers
from user.models import User, EmailVerifyTable, PhoneVerifyTable, bvnVerifyTable, BeneficiaryTable

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmailVerifyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifyTable
        fields = '__all__'

class PhoneVerifyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerifyTable
        fields = '__all__'

class bvnVerifyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = bvnVerifyTable
        fields = '__all__'

class BeneficiaryTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficiaryTable
        fields = '__all__'
