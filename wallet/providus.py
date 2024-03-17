import requests
import hashlib
from django.http import JsonResponse
from .models import Transaction,Wallet
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

def create_naira_account(user):
    url =  "http://154.113.16.142:8088/appdevapi/api/"+ 'PiPCreateReservedAccountNumber'
    data = {
            "account_name":"james bolton",
            "bvn":"2225678990"
            }
    headers={
       "Content-Type":"application/json",
       "Client-Id":"dGVzdF9Qcm92aWR1cw==",
       "X-Auth-Signature":"BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7",
    }

    print("jjjjjjjjjjjjjjjjjjjjjjjjjj")
    try:
        response=requests.post(url, json = data, headers =headers)
    except:
        return None
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        print(response_data["responseCode"], response_data["account_number"])
        return response_data['responseCode'], response_data["account_number"], response_data["account_name"]
    else:
        return None

def verify_naira_payment(settlementid):
    url =  "http://154.113.16.142:8088/appdevapi/api/"+ 'PiPverifyTransaction_settlementid?settlement_id='+ settlementid

    headers={
       "Content-Type":"application/json",
       "Client-Id":"dGVzdF9Qcm92aWR1cw==",
       "X-Auth-Signature":"BE09BEE831CF262226B426E39BD1092AF84DC63076D4174FAC78A2261F9A3D6E59744983B8326B69CDF2963FE314DFC89635CFA37A40596508DD6EAAB09402C7",
    }

    print("jjjjjjjjjjjjjjjjjjjjjjjjjj")
    try:
        response=requests.post(url, headers =headers)
    except:
        return None
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        print(response_data["transactionAmount"], response_data["accountNumber"])
        return response_data['transactionAmount']
    else:
        return None
def check_for_settlement_duplicate(settlementId):
    trans=Transaction.objects.filter(settlementId=settlementId).exists()
    if trans:
        return False
    else:
        return True

def check_account_number_exists(account_number):
    try:
        # Check if there is any wallet with the specified account number and currency code "NGN"
        wallet = Wallet.objects.get(account_number=account_number, currency_code="NGN")
        return True
    except Wallet.DoesNotExist:
        return False

def bank_webhook(request):
    # Replace these values with your actual ClientId and ClientSecret
    client_id = "your_client_id"
    client_secret = "your_client_secret"

    # Verify X-Auth-Signature
    x_auth_signature = request.headers.get("X-Auth-Signature")
    expected_signature = hashlib.sha512(f"{client_id}:{client_secret}".encode("utf-8")).hexdigest()
    if x_auth_signature != expected_signature:
        return JsonResponse(
            {
                "requestSuccessful": True,
                "responseCode": "02",
                "sessionId":"99990000554443332221",
                "responseMessage":"rejected transaction"
            },
            status=400,
        )

    # Parse the request body
    request_data = request.json()

    # Extract the necessary fields from the request data
    session_id = request_data.get("sessionId")
    settlementId = request_data.get("settlementId")
    accountnumber =request_data.get("accountNumber")
    # Add any other required fields from the request data

    # Perform your verification logic based on the extracted data
    # For example, check for duplicate settlement ID or validate the account number
    verifyaccount=check_account_number_exists(accountnumber)
    if not verifyaccount:
        # Return the appropriate response
        response_data = {
        "requestSuccessful": True,
        "sessionId": session_id,
        "responseMessage": "rejected transaction",
        "responseCode": "02"
        }
        return JsonResponse(response_data)
    verifypayment=verify_naira_payment(settlementId)
    if verifypayment is not None:
        if check_for_settlement_duplicate(settlementId):
        # Return the appropriate response
            response_data = {
                "requestSuccessful": True,
                "sessionId": session_id,
                "responseMessage": "duplicate transaction",
                "responseCode": "01"
            }
            return JsonResponse(response_data)
        else:
   # Add the transaction to the database
            wallet = Wallet.objects.get(account_number=accountnumber, currency_code="NGN")
            
            transaction = Transaction.objects.create(
                user=wallet.user,
                name="Payment",
                transaction_type="debit",
                transaction_id=settlementId,
                reference_id=session_id,  # Replace with your reference ID logic
                currency_code="NGN",
                amount=Decimal(verifypayment),
                remainbalance=wallet.balance,
                sourceAccountNumber=request_data.get("sourceAccountNumber"),
                sourceBankName=request_data.get("sourceBankName"),
                sourceAccountName=request_data.get("sourceAccountName"),

                settlementId=settlementId
            )

    wallet = Wallet.objects.get(account_number=accountnumber, currency_code="NGN")
    wallet.balance += Decimal(verifypayment)
    wallet.save()
    # Return the appropriate response
    response_data = {
        "requestSuccessful": True,
        "sessionId": session_id,
        "responseMessage": "success",
        "responseCode": "00",
    }
    return JsonResponse(response_data)
