import os
from flask import Flask, request, render_template, redirect, abort, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_caching import Cache
import requests


load_dotenv()

app = Flask(__name__)

app.config.from_object(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

CORS(app, resources={r"/*":{'origins':"*"}})


@cache.memoize(timeout=3600)
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



@cache.memoize(timeout=3600)
def create_transfer_recipient(payload):
    '''Sends names, account number, account type, currency and bank code to get account information'''
    
    response = requests.post('https://api.paystack.co/transferrecipient', 
        headers = {
            'Authorization': f'Bearer {os.getenv("SECRET_KEY")}',
            'Content-Type': 'application/json'
            },
        json = {"type": payload["account_type"],
            "name": f'{payload["first_name"].lower()} {payload["last_name"].lower()}',
            "account_number": payload["account_number"],
            "bank_code": payload["bank_code"],
            "currency": payload["currency"]
            },
        )
    return response.json()



@cache.memoize(timeout=3600)
def list_available_banks(country):
    '''Gets a list of available banks in the country and their neccessary information such as bank code, etc.'''
    
    response = requests.get('https://api.paystack.co/bank', 
            params={
                'country':country,
            },
        )
    return response.json()


@cache.memoize(timeout=3600)
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
    return response.json()







@app.route("/", methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        abort(405)

@app.route("/verify", methods=['GET','POST'])
@cache.memoize(timeout=3600)    #Cache memorize stores results per arguments for the next hour  
def resolve_account():
    '''
        Verifies the owner of the account using the account number 
        and bank code. 
    '''
    if request.method == 'POST':
        data = get_account_info(request.form.get('account_number'), request.form.get('bank_code'))
        
        return render_template('index.html', r_account=data)    #Page refreshes to show response/result
    
    elif request.method == 'GET':
        return redirect('/')
    
    else:
        abort(405)


@app.route("/create-recipient", methods=['GET','POST'])
@cache.memoize(timeout=3600)   #Cache memorize stores results per arguments for the next hour
def create_recipient():
    '''
        Creates/confirms a transfer recipient, using account owner's names,
        account number and bank code of the bank 
    '''
    if request.method == 'POST':
        try:
            user_data = {
                "first_name": request.form.get('first_name'),
                "last_name": request.form.get('last_name'),
                "account_number":  request.form.get('account_number'),
                "bank_code": request.form.get('bank_code'),
                "account_type":  request.form.get('type'),
                "currency": request.form.get('currency')
            }
        except:
            abort(403)
        
        data = create_transfer_recipient(user_data)
        return render_template('index.html', t_recipient=data)    #Page refreshes to show response/result
    
    elif request.method == 'GET':
        return redirect('/')
    
    else:
        abort(405)
    

@app.route("/get-banks", methods=['GET','POST'])
# @cache.memoize(timeout=3600)    #Cache memorize stores results per arguments for the next hour
def get_bank_list():
    '''
        Returns list of banks in specified country i.e Nigeria or Ghana
    '''
    if request.method == 'POST':
        data = list_available_banks(f"{request.form.get('country')}")
        
        return render_template('index.html', banks=data)    #Page refreshes to show response/result
   
    elif request.method == 'GET':
        return redirect('/')
    
    else:
        abort(405)
    

@app.route('/initialize-transaction', methods=["GET", "POST"])
@cache.memoize(timeout=3600)    #Cache memorize stores results per arguments for the next hour
def initialize_transaction():
    '''
        Creates a link to the payment using customers email and price to be paid
    '''
    if request.method == 'POST':
        link = get_payment_link(request.form.get('email'), request.form.get('amount'))
        
        return render_template('index.html', tr_link=link)  #Page refreshes to show response/result
    
    elif request.method == 'GET':
        return redirect('/')
    
    else:
        abort(405)
    

#Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify ({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify ({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405
    

@app.errorhandler(403)
def bad_request(error):
    return jsonify ({
        "success": False,
        "error": 403,
        "message": "Bad request"
    }), 403

@app.errorhandler(400)
def bad_request(error):
    return jsonify ({
        "success": False,
        "error": 403,
        "message": "Bad request"
    }), 403


if __name__== "__main__":
    app.run(debug=True)