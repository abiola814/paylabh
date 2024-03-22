import requests
import random
import string
import hashlib
import base64
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

def generate_basic_auth(username, password):
    credentials = f"{username}:{password}"
    credentials_bytes = credentials.encode('ascii')
    encoded_credentials = base64.b64encode(credentials_bytes)
    auth_header = f"Basic {encoded_credentials.decode('ascii')}"
    return auth_header



def generate_random_alphanumeric(length):
    alphanumeric_characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(alphanumeric_characters) for _ in range(length))

def createNairaAccount(user):
    referenceNumber = generate_random_alphanumeric(16)
    username="Paylab_User"
    combined_string = f"{referenceNumber}:{username}"
    hashed_value = hashlib.sha512(combined_string.encode()).hexdigest()
    print(generate_basic_auth(username,hashed_value))
    headers={
       "Content-Type":"application/json",
       "Authorization":generate_basic_auth(username,hashed_value)
    }
    data=json.dumps({
      "requestHeader": {
        "clientId": "400889PTPV595",
        "requestType": "Bank Transfer"   
    },
    
        "customerName": f"{user.first_name} {user.last_name}",
        "referenceNumber": referenceNumber ,
        "customerID ": user.id
    })
    url = "http://sandbox1.coralpay.com:8080/paywithtransfer/moneytransfer/apis/staticAccount"
    try:
        response = requests.request("POST", url, headers=headers, data=data)
    except:
        return None
    print(response.json())
    print(response)
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        print(response_data["responseDetails"]["responseCode"], response_data["accountNumber"])
        return response_data["responseDetails"]['responseCode'], response_data["accountName"], response_data["accountNumber"],response_data["nameOfBank"]
    else:
        return None


@csrf_exempt
def coralpay_webhook(request):
    USERNAME=""
    PASSWORD=""
    if request.method == 'POST':
        # Check if request contains authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'Authorization header is missing'}, status=401)

        # Extract username and password from authorization header
        try:
            auth_type, auth_credentials = auth_header.split(' ')
            if auth_type.lower() != 'basic':
                raise ValueError("Unsupported authorization type")

            auth_decoded = base64.b64decode(auth_credentials).decode('utf-8')
            auth_username, auth_password = auth_decoded.split(':')
        except (ValueError, UnicodeDecodeError):
            return JsonResponse({'error': 'Invalid authorization header'}, status=401)

        # Check if username and password match
        if auth_username != USERNAME or auth_password != PASSWORD:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)

        # Check if JSON data is present in the request
        try:
            notification_data = request.json()
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Extract notification data from JSON payload
        try:
            account_number = notification_data['account_number']
            account_name = notification_data['account_name']
            transaction_amount = Decimal(notification_data['transaction_amount'])
            module_value = notification_data['module_value']
        except KeyError:
            return JsonResponse({'error': 'Missing required fields in notification data'}, status=400)

        # Calculate module value
        computed_module_value = hashlib.sha512(
            (account_number + account_name + str(transaction_amount)).encode()
        ).hexdigest()

        # Compare computed module value with received module value
        if computed_module_value != module_value:
            return JsonResponse({'error': 'Module value mismatch. Potential data integrity issue'}, status=400)

        # Process the notification and create a transaction
        # Example: Create a transaction using the received data
        # Replace this with your actual transaction creation logic
        # transaction = create_transaction(account_number, account_name, transaction_amount)

        return JsonResponse({'success': 'Transaction created successfully'})

    return JsonResponse({'error': 'Unsupported method'}, status=405)