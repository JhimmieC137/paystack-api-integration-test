import os
import sys
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


payload = {
    "first_name": "DAVID",
    "last_name": "OLUJIMI",
    "account_type": "nuban",
    "account_number": 2230914852,
    "bank_code": "033",
    "currency": "NGN",
    "email": "toluwalope.david@gmail.com",
    "amount": 2000,
    "sample_country": "Nigeria"
}

errload = {
    "last_name": "Joji",
    "account_type": "nuban",
    "account_number": 2340914852,
    "bank_code": "031",
    "currency": "NGN",
    "email": "toololole.draked@rocketmail.com",
    "amount": 2000,
    "sample_country": "South"
}

    
def test_resolve_account():
    response = requests.post(f'http://{os.getenv("DEV_BASE_URL")}/verify',
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}'
        },
        data = {
            'account_number': payload['account_number'],
            'bank_code': payload["bank_code"]
        })
    
    assert response.status_code == 200
    
def test_err_resolve_account():
    response = requests.patch(f'http://{os.getenv("DEV_BASE_URL")}/verify',
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}'
        },
        data = {
            'account_number': errload['account_number'],
            'bank_code': errload["bank_code"]
        })
    
    assert response.status_code == 405


    
def test_get_bank_list():
    response = requests.post(f'http://{os.getenv("DEV_BASE_URL")}/get-banks',
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}'
        },
        data = {
            'country': errload['sample_country'],
        })
    assert response.status_code == 200


    
def test_err_get_bank_list():
    response = requests.put(f'http://{os.getenv("DEV_BASE_URL")}/get-banks',
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}'
        },
        data = {
            'country': errload['sample_country'],
        })
    assert response.status_code == 405

    
def test_initialize_transaction():
    response = requests.post(f'http://{os.getenv("DEV_BASE_URL")}/initialize-transaction',
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}'
        },
        data = {
            'email': payload['email'],
            'amount': payload['amount']
        })
    assert response.status_code == 200

    
def test_err_initialize_transaction():
    response = requests.post(f'http://{os.getenv("DEV_BASE_URL")}/initialize-transactions',
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}'
        },
        data = {
            'email': errload['email'],
            'amount': errload['amount']
        })
    assert response.status_code == 404
