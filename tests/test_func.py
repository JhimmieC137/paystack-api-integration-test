import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app import get_account_info, create_transfer_recipient, list_available_banks, get_payment_link

 
payload = {
    "first_name": "David",
    "last_name": "Olujimi",
    "account_type": "nuban",
    "account_number": 2230914852,
    "bank_code": "033",
    "currency": "NGN",
    "email": "toluwalope.david@gmail.com",
    "amount": 2000,
    "sample_country": "Nigeria"
}

errload = {
    "first_name": "Zoey",
    "last_name": "Joji",
    "account_type": "nuban",
    "account_number": 2340914852,
    "bank_code": "031",
    "currency": "NGN",
    "email": "toololole.draked@rocketmail.com",
    "amount": 2000,
    "sample_country": "Togo"
}


def test_get_account_info():
    response = get_account_info(payload["account_number"], payload["bank_code"])
    assert response['data']['account_name'] == "DAVID TOLOWALOPE OLUJIMI"
    assert response['data']['bank_id'] == 18
    assert response['status'] == True


def test_err_get_account_info():
    response = get_account_info(errload["account_number"], errload["bank_code"])
    assert response['status'] == False
    assert 'Could not resolve account name' in response['message']
    

def test_create_transfer_recipient():
    response = create_transfer_recipient(payload)
    assert response['data']['details']['bank_name'] == 'United Bank For Africa'
    assert response['data']['details']['bank_code'] == '033'
    assert response['status'] == True
    

def test_err_create_transfer_recipient():
    response = create_transfer_recipient(errload)
    assert response['status'] == False
    assert 'Cannot resolve account' in response['message']
    

def test_list_available_banks():
    response = list_available_banks(payload["sample_country"])
    assert response['status'] == True
    assert response['message'] == 'Banks retrieved'

def test_err_list_available_banks():
    response = list_available_banks(errload["sample_country"])
    assert response['data'] == []
    
    
def test_get_payment_link():
    response = get_payment_link(payload['email'], payload['amount'])
    assert response['status'] == True
    assert response['data']['access_code'] in response['data']['authorization_url']
    assert response['message'] == 'Authorization URL created'
    
    
def test_err_get_payment_link():
    response = get_payment_link(errload['email'], errload['amount']/10000)
    assert response['status'] == False
    

        