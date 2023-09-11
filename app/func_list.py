import requests
import os

def get_account_info(account_number, bank_code):
    '''Sends account number and bank code of the bank to get account information'''
    
    response = requests.get('https://api.paystack.co/bank/resolve', 
        params={
            'account_number': f'{account_number}',
            'bank_code': f'{bank_code}'
        },
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}'
            },
        )
    return response.json()


def create_transfer_recipient(payload):
    '''Sends names, account number, account type, currency and bank code to get account information'''
    
    response = requests.post('https://api.paystack.co/transferrecipient', 
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}',
            'Content-Type': 'application/json'
            },
        json = {"type": payload["account_type"],
            "name": f'{payload["first_name"]} {payload["last_name"]}',
            "account_number": payload["account_number"],
            "bank_code": payload["bank_code"],
            "currency": payload["currency"]
            },
        )
    return response.json()


def list_available_banks(country):
    '''Gets a list of available banks in the country and their neccessary information such as bank code, etc.'''
    
    response = requests.get('https://api.paystack.co/bank', 
            params={
                'country':country.lower()
            },
        )
    return response.json()

def get_payment_link(email, amount):
    '''Gets an authorized payment link'''
    
    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        headers={
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}',
            'Content-Type': 'application/json'
            },
        json={
            "email": email,
            "amount": amount
        })
    print(response.json())
    
    return response.json()
