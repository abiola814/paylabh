from billPayment.bills import walletProcess
from user.models import User
from wallet.serializer import TransactionSerializer
from wallet.models import Transaction,Chargefee
from datetime import datetime
import uuid
import math
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import secrets
import string
from user.utils import log_request
import re
from django.core.mail import send_mail, BadHeaderError
def labtransfer(request,amount,labName,id,ref_id,trans_id,charge):
    debit_amount = int(amount) + charge
    if not walletProcess(amount=debit_amount,user=request.user,id=id,type=1):
        return "insufficient balance","failed"
    if not walletProcess(amount=debit_amount,user=request.user,type=2,id=id):
        return "unable to debit wallet","failed"

    taguser= labName.replace('@LabTag',"")
    user= User.objects.get(tag__iexact=taguser)
    if walletProcess(amount=amount,user=user,type=3,id=id):
        balance = walletProcess(user=user,type=4,id=id)
        trans = Transaction.objects.create(user=user,name=f"{user.last_name} {user.first_name}",
    transaction_type="Credit",transaction_id=trans_id ,reference_id= ref_id,status="Success",
    description=f"transfer from  {request.user.last_name}",remainbalance=balance,amount=amount)
        return {
            "name":f"{user.first_name} {user.last_name}",
            "amount":amount,
            "transId":trans_id,
            "time":datetime.now(),
            "charge":charge,
            "sender":f"{request.user.first_name} {request.user.last_name}"
        },"success"
    else:
        return "unable to credit other account contact the customer care","reverse"

    
def calculate_charge_fee(name,amount):
    fee=Chargefee.objects.get(chargeTitle=name)
    if fee.ispercentage:
        charge=amount * fee.value
        if charge > 100:
            charge= 100
    else:
        charge=fee.value
    return {"amount":amount,"chargeFee":math.ceil(charge)}




def send_debit_mail(email,c):
    subject = "Welcome Message"
    email_template_name = "transaction_sent.html"

    email_template = render_to_string(email_template_name, c)
    try:
        send=EmailMessage(subject,email_template,'supports@paylab.finance' , [email])
        send.content_subtype="html"
        send.send()
    except Exception as e:
        log_request(e)

def send_credit_mail(email,c):
    subject = "Welcome Message"
    email_template_name = "transaction_receive.html"

    email_template = render_to_string(email_template_name, c)
    try:
        send=EmailMessage(subject,email_template,'supports@paylab.finance' , [email])
        send.content_subtype="html"
        send.send()
    except Exception as e:
        log_request(e)