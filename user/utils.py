import logging
from datetime import date
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from datetime import datetime
import uuid
import requests
from .models import User,EmailVerifyTable,PhoneVerifyTable
import environ
import os
from django.template.loader import render_to_string
import secrets
import string
import re
from django.core.mail import send_mail, BadHeaderError
# Initialise environment variables
env = environ.Env()

environ.Env.read_env(os.path.join('.env'))
def generateCode(number):
    # Define the length of the verification code
    code_length = number

    # Define the characters to use in the verification code
    characters = string.digits

    # Generate a random verification code
    verification_code = ''.join(secrets.choice(characters) for i in range(code_length))

    return verification_code
def log_request(*args):
    for arg in args:
        logging.info(arg)


def checkRequest(id,data):
    print(data)
    log_request(f"referenceId:{id},{data}")
    if data is None:
        log_request(f"detail:add json format")
        response ={ 'requestTime':datetime.now(),'referenceId':'id',"requestType":"outbound",
        "message":"Please , add your data json",
        "status":False,
        }
        return Response(data=response,status=status.HTTP_400_BAD_REQUEST)

def errorResponse(id,msg):
    response ={ 'requestTime':datetime.now(),'referenceId':id,"requestType":"outbound",
                "message": msg,
                "status":False
                }
    log_request(f"{response}")
    return Response(data=response,status=status.HTTP_400_BAD_REQUEST)


def successResponse(id,msg,extraname=None,extradata=None):

    if extraname == None:
        response ={ 'requestTime':datetime.now(),'referenceId':id,
                "requestType":"outbound",
                "message":msg,
                "status":True,
                        }
        log_request(f"{response}")
        return Response(data=response,status=status.HTTP_200_OK)
    else:
        response ={ 'requestTime':datetime.now(),'referenceId':id,
                "requestType":"outbound",
                "message":msg,
                "status":True,
                "data":{
                    extraname:extradata
                }
        }
        log_request(f"{response}")
        return Response(data=response,status=status.HTTP_200_OK)
def validatingPassword(password):
    if len(password) < 8:
        return "password must not be less than 8 digit"
    
    if not re.findall('\d', password):
        return "The password must contain at least 1 digit"
    if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
        return "Your password must contain at least 1 symbol"
    if not re.findall('[a-z]', password):
        return "Your password must contain at least 1 lowercase letter, a-z."
    if not re.findall('[A-Z]', password):
        return "Your password must contain at least 1 Uppercase letter, a-z."

    return True

def send_activation_mail(id,mail):
    subject = "Account activation code"
    email_template_name = "activation_email.txt"
    
    code = generateCode(6)
    c = {
    "email":mail,
    'domain':'localhost',
    'site_name': 'Website',
    'protocol': 'http',
    'code':code
    }

    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, 'partytime@mjobi.com' , [mail], fail_silently=False)
        if EmailVerifyTable.objects.filter(email=mail).exists():
            pass
        else:
            EmailVerifyTable(email=mail,code=code).save()
        return successResponse(id,f"check your {mail} to activate it",None,None)
    except:

        return errorResponse(id,f"unable to send to email activation code to {mail}")

def send_activation_phone(id,phone):
    if PhoneVerifyTable.objects.filter(phone=phone).exists():
        pass
    else:
        PhoneVerifyTable(phone=phone,code=123457).save()
    return successResponse(id,f"code sent to {phone}")