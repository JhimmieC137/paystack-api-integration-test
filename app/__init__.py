import os
import uuid
from .func_list import get_account_info, create_transfer_recipient, list_available_banks, get_payment_link
from flask import Flask, request, render_template, redirect, abort, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})


@app.route("/", methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        abort(405)

@app.route("/verify", methods=['GET','POST'])
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