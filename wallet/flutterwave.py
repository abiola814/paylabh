import requests

def create_naira_account(user):
    url =  "https://api.flutterwave.com/v3/"+ 'payout-subaccounts'
    data = {
            "account_name":f"{user.first_name} {user.last_name}",
            "email": user.email,
            "mobilenumber": user.phone,
            "country": "NG",
            "account_reference":user.reference,
            "bank_code": "035"
            }
    headers={
        "Authorization":"Bearer "+ "FLWSECK_TEST-e3a50c9e6203cc6c1b564bdd0589dfd5-X"
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
        print(response_data['status'], response_data["data"])
        return response_data['status'], response_data["data"]
    else:
        return None

def check_naira_account_bal(ref):

    url =  "https://api.flutterwave.com/v3/"+ 'payout-subaccounts/' + str(ref) + "/balances" 

    headers={
        "Authorization":"Bearer "+ "FLWSECK_TEST-e3a50c9e6203cc6c1b564bdd0589dfd5-X"
    }

    print("jjjjjjjjjjjjjjjjjjjjjjjjjj")
    try:
        response=requests.get(url, headers =headers)
    except:
        return None
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        print(response_data['status'], response_data["data"])
        return response_data['status'], response_data["data"]
    else:
        return None

def check_naira_account_bal(ref):

    url =  "https://api.flutterwave.com/v3/"+ 'payout-subaccounts/' + str(ref) + "/balances" 

    headers={
        "Authorization":"Bearer "+ "FLWSECK_TEST-e3a50c9e6203cc6c1b564bdd0589dfd5-X"
    }

    print("jjjjjjjjjjjjjjjjjjjjjjjjjj")
    try:
        response=requests.get(url, headers =headers)
    except:
        return None
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        print(response_data['status'], response_data["data"])
        return response_data['status'], response_data["data"]
    else:
        return None

def buy_airtime(network,number,amount,ref):

    url =  "https://ruggedwallet.com.ng/api/topup/" 

    headers={
        "Authorization":"Token "+ "YmM4YTk2OTUxZTg4MjU2ODJjMmI2NTMxYjg0ZmUzMmQ1OTlhNmE5ODI3MTFjOTFhZDMxZTVhY2I5YjVh"
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
        response=requests.get(url, headers =headers ,data=data)
    except:
        return None
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        print(response_data['status'])
        return response_data['status']
    else:
        return None

def buy_data(network,dataplan,number,amount,ref):

    url =  "https://ruggedwallet.com.ng/api/data/" 

    headers={
        "Authorization":"Token "+ "YmM4YTk2OTUxZTg4MjU2ODJjMmI2NTMxYjg0ZmUzMmQ1OTlhNmE5ODI3MTFjOTFhZDMxZTVhY2I5YjVh"
    }
    data ={
        "network": network,
        "phone": number,
        "data_plan": dataplan,
        "bypass": False,
        "request-id": ref,
        "amount":amount
    }
    try:
        response=requests.get(url, headers =headers ,data=data)
    except:
        return None
    print(response.json())
    # checking the status code
    if response.status_code == 200:
        response_data = response.json()
        # passing the stsatus data and other  info data to the class view Payment
        print(response_data['status'])
        return response_data['status']
    else:
        return None
