from wallet.models import Transaction,Wallet
from rest_framework import serializers
from rest_framework.validators import ValidationError
from random import randrange
from .models import NetworkType,DataBundle,Cable,Bills,Exam




class DataBundleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=DataBundle
        fields = ("id","networkType","dataplan","day","size","amount","unique_id")
        
class NetworkSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=NetworkType
        fields = ("id","network","unique_id","image_url")

        
class CableSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Cable
        fields = ("id","name","cable_id","planname","cableplan","amount")
        
class BillsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Bills
        fields = ("id","disco","meter_type","unique_id")
        
class ExamSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Exam
        fields = ("id","name","unique_id","amount")
