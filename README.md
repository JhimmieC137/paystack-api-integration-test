# Paystack API Integration
Paystack is a Nigerian financial technology company that offers payment processing services to businesses. They have used different tools and technologies to make their services easily accessible and efficient enough to reduce payment issues. Paystack's API is one of the major ways to use their services for transacions on mobile and web applications. This project demonstrates how it works using a few endpoints.

## About the stack
This project consists of a light-weight python application, using the Flask framework on the backend. On the frontend, regular HTML, CSS and Javascriptis used to render information fetched from the backend. As such all success and error reports from the Paystack API are rendered to the frontend in a user friendly manner.

## Available endpoints

### _home_ ('/'):
This is the landing page of the application. It returns a rendering of the homepage and only page of the application.
Methods allowed: 'GET'

### _initialize_transaction_ ('/initialize-transaction'):
It takes in form data to Initialize a transaction from your backend, by generating a link to a payment page. Sending a request, payload should be added as form data in the format:
```
        data = {
            'email': '{a vald account number}',
            'amount': {a non zero integer}
        }
```
Methods allowed: 'GET' 'POST'

### _get_bank_list_ ('/get-banks'):
This endpoint uses a function that fetches data on every bank within a specified country that uses paystack's services i.e Nigeria, Ghana and South Africa. If a different country is specified, it returns an empty list. Sending a request, payload should be added as form data in the format:
```
        data = {
            'country': '{specified country}'
        }
```
Methods allowed: 'GET' 'POST'

### _resolve_account_ ('/verify'):
The purpose of the endpoint is to verify the details of the user before initiating a transaction. It'll require the user's bank account number and the bank's unique code(this can be gotten from the bank list api). It returns name and other details concerning the account if data is valid. Sending a request, payload should be added as form data in the format:
```
        data = {
            'account_number': {a valid bank account number},
            'bank_code': '{the respective bank code}'
        }
```
Methods allowed: 'GET' 'POST'

### _create_recipient_ ('/create-recipient'):
This endpoint is silimar to the _resolve_account_ endpoint. It requires details like the user's name, account number, bank code,  currency and account type, which are all used to create a transfer recipient object containing more information on the account. Sending a request, payload should be added as form data in the format:
```
        data = {
            'first_name': '{first name}',
            'last_name': '{last name}',
            'account_type': '{'nuban' for Nigerian accounts and 'mobile-money' for Ghanian accounts}'
            'currency': '{'NGN' for Nigerian accounts and 'GHS' for Ghanian accounts }'
            'account_number': {a valid bank account number},
            'bank_code': '{the respective bank code}'
        }
```
Methods allowed: 'GET' 'POST'

### Pop-up checkout:
This is no endpoint and has no connection to the flask apllication in this project, it is handled by some lines of inline Javascript code on the frontend that sends and fetches data to and from paystacks API and pops up a payment portal after submitting names, emailand and amount to be paid.

#### Note
Data types for form data should be:
- first_name : str
- last_name: str
- bank_code: str
- account_number: int(non negative)
- amount: int(non negative)
- email: str
- account_type: str
- country: str

All requests made to the paystack API will require a SECRET KEY from a developers account on [paystack's website](https://dashboard.paystack.com/#/signup). This has been provided in a .env file on the live application @ [jimi.theupfolio.com]('https://jimi.theupfolio.com') 

## Setting up
To run this application on your local machine, you'll need to have [python 3](https://www.python.org/downloads/release/python-390/) installed and have a developers account with paystack. Clone this repo @ [https://github.com/JhimmieC137/paystack-api-integration-test](https://github.com/JhimmieC137/paystack-api-integration-test/), create a virtual environment 

```
linux: virtualenv env && source env/bin/activate

windows: python3 -m venv env 
        venv\scripts\activate
```

Install the packages listed in the requirements.txt file
```
pip install -r requirements.txt
```
Create a .env file and fill in the details

```
FLASK_DEBUG=False   #Changes to True in production

SECRET_KEY = {the secret key from your paystack account}

DEV_BASE_URL = {'localhost:5000' depending on what port you'll like to run the app on}

PROD_BASE_URL = {production url}
```

Then run the command `flask run`

## Testing
To run the unit and integrations tests on the app, navigate to the `tests` folder and run the command `python pytest`.

This application as also been deploeyed to a live server @ [jimi.theupfolio.com](https://jimi.theupfolio.com/)
