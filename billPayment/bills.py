
import logging
from datetime import date
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from datetime import datetime
import uuid
import requests
import environ
import os
from django.template.loader import render_to_string
import secrets
import string
import json
import re
from wallet.serializer import TransactionSerializer
from user.utils import log_request
from wallet.models import Wallet
from user.models import User
from wallet.models import Transaction
from django.core.mail import send_mail, BadHeaderError
# Initialise environment variables
env = environ.Env()

environ.Env.read_env(os.path.join('.env'))

def walletProcess(currency="NGN",amount=None,user=None,type=None,id=None):
    userinfo = User.objects.get(id = user.id)
    if Wallet.objects.filter(currency_code=currency,user=userinfo).exists():
        ...
    else:
        return False
        
    if type == 1:
        # 1 mean check if user have sufficent balance
        check_user_balance = Wallet.objects.get(currency_code=currency,user=userinfo)
        if check_user_balance.balance >= int(amount):
            return True
        else:
            return False
    if type == 2:
        # 2 mean  for debit on user wallet account
        user_wallet = Wallet.objects.get(currency_code=currency,user=userinfo)
        user_wallet.balance -= int(amount)
        user_wallet.save()
        log_request(f" reference {id} user is debit with {amount}")
        return True
    if type == 3:
        # 3 mean  for credit on user wallet account
        user_wallet = Wallet.objects.get(currency_code=currency,user=userinfo)
        user_wallet.balance += int(amount)
        user_wallet.save()
        log_request(f" reference {id} user is credit with {amount}")
        return True
    if type == 4:
        # 4 mean check user balance
        user_balance = Wallet.objects.get(currency_code=currency,user=userinfo)
        return user_balance.balance

def buy_airtime(request,network,number,amount,ref,id):

    if not walletProcess(amount=amount,user=request.user,id=id,type=1):
        return "insufficient balance","failed"
    if not walletProcess(amount=amount,user=request.user,type=2,id=id):
        return "unable to debit wallet","failed"

    url =  "https://ruggedwallet.com.ng/api/topup/" 

    headers={
        "Authorization":"Token "+ "YmM4YTk2OTUxZTg4MjU2ODJjMmI2NTMxYjg0ZmUzMmQ1OTlhNmE5ODI3MTFjOTFhZDMxZTVhY2I5YjVh",
        "Content-Type":"application/json"
    }
    data ={
        "network": network,
        "phone": number,
        "plan_type": "VTU",
        "bypass": False,
        "request-id": ref,
        "amount": amount
    }
    try:
        response=requests.post(url, headers =headers, data=json.dumps(data))
    except:
        return "try again"
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        trans={
            "user":request.user.id,
            "transaction_type":"debit",
            "transction_id":response_data["request-id"],
            "status":"Success",
            "currency_code":"NGN",
            "amount":amount,
            "reference_id": ref,
            "remainbalance": walletProcess(user=request.user,type=4),
            "name": f"{response_data['network']} airtime"

        }
        serializer_data=TransactionSerializer(data=trans, context={"request": request})
        if serializer_data.is_valid():
            serializer_data.save()
            return f"{number} credited with {amount}",response_data["status"]
        else:
            return serializer_data.errors,"failed"
    elif response.status_code ==400:
        response_data = response.json()
        return response_data['msg'],"failed"
        

def buy_data(network,dataplan,number,amount,ref,request,id):

    if not walletProcess(amount=amount,user=request.user,id=id,type=1):
        return "insufficient balance","failed"
    if not walletProcess(amount=amount,user=request.user,type=2,id=id):
        return "unable to debit wallet","failed"

    url =  "https://ruggedwallet.com.ng/api/data/" 

    headers={
        "Authorization":"Token "+ "YmM4YTk2OTUxZTg4MjU2ODJjMmI2NTMxYjg0ZmUzMmQ1OTlhNmE5ODI3MTFjOTFhZDMxZTVhY2I5YjVh",
     "Content-Type":"application/json"
    }
    data ={
        "network": network,
        "phone": number,
        "data_plan": dataplan,
        "bypass": False,
        "request-id": ref,
        
    }
    print(data)
    try:
        response=requests.post(url, headers =headers, data=json.dumps(data))
    except:
        return "try again","failed"
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        trans={
            "user":request.user.id,
            "transaction_type":"debit",
            "transction_id":response_data["request-id"],
            "status":"Success",
            "currency_code":"NGN",
            "amount":amount,
            "reference_id": ref,
            "remainbalance": walletProcess(user=request.user,type=4),
            "name": f"{response_data['network']} data"

        }
        serializer_data=TransactionSerializer(data=trans, context={"request": request})
        if serializer_data.is_valid():
            serializer_data.save()
            return f"{number} credited with {amount}",response_data["status"]
        else:
            return serializer_data.errors,"failed"
    elif response.status_code ==400:
        response_data = response.json()
        return response_data['msg'],"failed"


# def buy_cable(request,cable_id,cableplan,iuc,amount,ref,id):

#     if not walletProcess(amount=amount,user=request.user,id=id,type=1):
#         return "insufficient balance","failed"
#     if not walletProcess(amount=amount,user=request.user,type=2,id=id):
#         return "unable to debit wallet","failed"

#     url =  "https://ruggedwallet.com.ng/api/cable/" 

#     headers={
#         "Authorization":"Token "+ "YmM4YTk2OTUxZTg4MjU2ODJjMmI2NTMxYjg0ZmUzMmQ1OTlhNmE5ODI3MTFjOTFhZDMxZTVhY2I5YjVh",
#      "Content-Type":"application/json"
#     }
#     data ={
#         "cable" : cable_id, 
#         "iuc" : iuc,
#          "cable_plan" : cableplan,
#         "bypass": False,
#         "request-id": ref,
        
#     }
#     print(data)
#     try:
#         response=requests.post(url, headers =headers, data=json.dumps(data))
#     except:
#         return "try again","failed"
#     print(response.json())
#     # checking the status code
#     if response.status_code == 200:
#         response_data = response.json()
#         # passing the stsatus data and other  info data to the class view Payment
#         trans={
#             "user":request.user.id,
#             "transaction_type":"debit",
#             "transction_id":response_data["request-id"],
#             "status":"Success",
#             "currency_code":"NGN",
#             "amount":amount,
#             "reference_id": ref,
#             "remainbalance": walletProcess(user=request.user,type=4),
#             "name": f"{response_data['plan_name']} cable"

#         }
#         serializer_data=TransactionSerializer(data=trans, context={"request": request})
#         if serializer_data.is_valid():
#             serializer_data.save()
#             return f"{iuc} funded with {amount} for {response_data['plan_name']}",response_data["status"]
#         else:
#             return serializer_data.errors,"failed"
#     elif response.status_code ==400:
#         response_data = response.json()
#         return response_data['msg'],"failed"



def buy_bills(request,disco,meter_type,meter_number,amount,ref,id):

    if not walletProcess(amount=amount,user=request.user,id=id,type=1):
        return "insufficient balance","failed"
    if not walletProcess(amount=amount,user=request.user,type=2,id=id):
        return "unable to debit wallet","failed"

    url =  "https://ruggedwallet.com.ng/api/bill/" 

    headers={
        "Authorization":"Token "+ "YmM4YTk2OTUxZTg4MjU2ODJjMmI2NTMxYjg0ZmUzMmQ1OTlhNmE5ODI3MTFjOTFhZDMxZTVhY2I5YjVh",
     "Content-Type":"application/json"
    }
    data ={
        "disco" : disco, 
        "meter_type" : meter_type, 
        "meter_number" : meter_number,
        "amount":amount,
        "bypass": False,
        "request-id": ref,
        
    }
    print(data)
    try:
        response=requests.post(url, headers =headers, data=json.dumps(data))
    except:
        return "try again","failed"
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        trans={
            "user":request.user.id,
            "transaction_type":"debit",
            "transction_id":response_data["request-id"],
            "status":"Success",
            "currency_code":"NGN",
            "amount":amount,
            "reference_id": ref,
            "remainbalance": walletProcess(user=request.user,type=4),
            "name": f"{disco} electricity paid",
            "reference":response_data

        }
        serializer_data=TransactionSerializer(data=trans, context={"request": request})
        if serializer_data.is_valid():
            serializer_data.save()
            return response_data,response_data["status"]
        else:
            return serializer_data.errors,"failed"
    elif response.status_code ==400:
        response_data = response.json()
        return response_data['msg'],"failed"
def buy_result(request,exam,quantity,amount,ref,id):
    amount= int(quantity) * int(amount)
    if not walletProcess(amount=amount,user=request.user,id=id,type=1):
        return "insufficient balance","failed"
    if not walletProcess(amount=amount,user=request.user,type=2,id=id):
        return "unable to debit wallet","failed"

    url =  "https://ruggedwallet.com.ng/api/exam/" 

    headers={
        "Authorization":"Token "+ "YmM4YTk2OTUxZTg4MjU2ODJjMmI2NTMxYjg0ZmUzMmQ1OTlhNmE5ODI3MTFjOTFhZDMxZTVhY2I5YjVh",
     "Content-Type":"application/json"
    }
    data ={
        "quantity" : quantity, 
        "exam" : exam, 
        
    }
    print(data)
    try:
        response=requests.post(url, headers =headers, data=json.dumps(data))
    except:
        return "try again","failed"
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        trans={
            "user":request.user.id,
            "transaction_type":"debit",
            "transction_id":ref,
            "status":"Success",
            "currency_code":"NGN",
            "amount":amount,
            "reference_id": ref,
            "remainbalance": walletProcess(user=request.user,type=4),
            "name": f"{exam} result payment",
            "reference":response_data

        }
        serializer_data=TransactionSerializer(data=trans, context={"request": request})
        if serializer_data.is_valid():
            serializer_data.save()
            return response_data,response_data["status"]
        else:
            return serializer_data.errors,"failed"
    elif response.status_code ==400:
        response_data = response.json()
        return response_data['msg'],"failed"




def coral_check(slug):

    url =  "http://204.8.207.124:8080/coralpay-vas/api/packages/biller/slug/" + slug

    headers = {
            'Authorization': 'Basic UGF5bGFiWDpQQHlsQGJ4NjclIw=='
    }

    try:
        response=requests.get(url, headers =headers)
    except:
        return "try again","failed"
    print(response.json())
    response_data = response.json()
    # checking the status code
    if response_data["error"] == False:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        return response_data["responseData"],"success"
    
    else:
        return  response_data["message"],"failed"



def all_cable(request=None,id=None):

    url =  "http://204.8.207.124:8080/coralpay-vas/api/billers/group/2"

    headers=headers = {
            'Authorization': 'Basic UGF5bGFiWDpQQHlsQGJ4NjclIw==',
    }


    response=requests.get(url, headers=headers)
    
    print(response.json())
    response_data = response.json()

    # checking the status code
    if response_data["error"] == False:
        return response_data["responseData"],"success"
    else:
        return "try again","failed"



def buy_coralpay(request,customer_number,paymentRef,slug,amount,id):

    if not walletProcess(amount=amount,user=request.user,id=id,type=1):
        return "insufficient balance","failed"
    if not walletProcess(amount=amount,user=request.user,type=2,id=id):
        return "unable to debit wallet","failed"

    url =  "http://204.8.207.124:8080/coralpay-vas/api/transactions/process-payment" 

    headers= {
            'Authorization': 'Basic UGF5bGFiWDpQQHlsQGJ4NjclIw==',
            'Content-Type': 'application/json'
    }
    data ={
            "paymentReference": paymentRef,
            "customerId": customer_number,
            "packageSlug":slug ,
            "channel": "WEB",
            "amount": amount,
            "customerName": request.user.last_name,
            "phoneNumber": request.user.phone,
            "email": request.user.email,
            "accountNumber": "0012345678"
            }
    print(data)
    try:
        response=requests.post(url, headers =headers, data=json.dumps(data))
    except:
        return "try again","failed"
    print(response.json())
    response_data = response.json()
    # checking the status code
    if response_data["error"] == False:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        trans={
            "user":request.user.id,
            "transaction_type":"debit",
            "transction_id":paymentRef,
            "status":"Success",
            "currency_code":"NGN",
            "amount":amount,
            "reference_id": paymentRef,
            "remainbalance": walletProcess(user=request.user,type=4),
            "name": ["responseData"]["customerMessage"] ,
            "reference":response_data

        }
        serializer_data=TransactionSerializer(data=trans, context={"request": request})
        if serializer_data.is_valid():
            serializer_data.save()
            return response_data["responseData"]["customerMessage"],"success"
        else:
            return serializer_data.errors,"failed"
        
    else:
        return response_data["message"],"failed"



def confirm_coralpay(customer_number,biller,slug):


    url =  "http://204.8.207.124:8080/coralpay-vas/api/transactions/customer-lookup" 

    headers= {
            'Authorization': 'Basic UGF5bGFiWDpQQHlsQGJ4NjclIw==',
            'Content-Type': 'application/json'
    }
    data ={
        "customerId": str(customer_number),
        "billerSlug": biller,
        "productName": slug
            }
    print(data)
    try:
        response=requests.post(url, headers =headers, data=json.dumps(data))
    except:
        return "try again","failed"
    print(response.json())
    response_data = response.json()
    # checking the status code
    if response_data["error"] == False:
        response_data = response.json()
        return response_data["responseData"],"success"
    else:
        return response_data["message"],"failed"


def all_electric(request=None,id=None):

    url =  "http://204.8.207.124:8080/coralpay-vas/api/billers/group/1"
    # url = "https://vas.coralpay.com/vas-service/api/biller-groups/1"
    

    headers=headers = {
            'Authorization': 'Basic UGF5bGFiWDpQQHlsQGJ4NjclIw==',
    }

    try:
        response=requests.get(url, headers =headers)
    except:
        return "try again","failed"
    print(response.json())
    response_data = response.json()

    # checking the status code
    if response_data["error"] == False:
        return response_data["responseData"],"success"
    else:
        return "try again","failed"

def all_bet(request=None,id=None):

    url =  "http://204.8.207.124:8080/coralpay-vas/api/billers/group/7"

    headers=headers = {
            'Authorization': 'Basic UGF5bGFiWDpQQHlsQGJ4NjclIw==',
    }

    try:
        response=requests.get(url, headers =headers)
    except:
        return "try again","failed"
    print(response.json())
    response_data = response.json()

    # checking the status code
    if response_data["error"] == False:
        return response_data["responseData"],"success"
    else:
        return "try again","failed"