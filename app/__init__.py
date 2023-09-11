import os
import uuid
from .func_list import get_account_info, create_transfer_recipient, list_available_banks, get_payment_link
from flask import Flask, request, render_template, redirect
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/verify", methods=['GET','POST'])
def resolve_account():
    '''
        Verifies the owner of the account using the account number 
        and bank code. 
    '''
    if request.method == 'POST':
        data = get_account_info(request.form.get('account_number'), request.form.get('bank_code'))
        return render_template('index.html', r_account=data)    #Page refreshes to show response/result
    else:
        return redirect('/')


@app.route("/create_recipient", methods=['GET','POST'])
def create_recipient():
    '''
        Creates/confirms a transfer recipient, using account owner's names,
        account number and bank code of the bank 
    '''
    if request.method == 'POST':

        user_data = {
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "account_number":  request.form.get('account_number'),
            "bank_code": request.form.get('bank_code'),
            "account_type":  request.form.get('type'),
            "currency": request.form.get('currency')
        }
        
        data = create_transfer_recipient(user_data)
       
        return render_template('index.html', t_recipient=data)    #Page refreshes to show response/result
    else:
        return redirect('/')
    

@app.route("/get_banks", methods=['GET','POST'])
def get_bank_list():
    '''
        Returns list of banks in specified country 
    '''
    if request.method == 'POST':
        data = list_available_banks(f"{request.form.get('country')}")
        return render_template('index.html', banks=data)    #Page refreshes to show response/result
    else:
        return redirect('/')
    

@app.route('/initialize-transaction', methods=["GET", "POST"])
def initialize_transaction():
    '''
        Creates a link to the payment using customers email and price to be paid
    '''
    if request.method == 'POST':
        link = get_payment_link(request.form.get('email'), request.form.get('amount'))
        return render_template('index.html', tr_link=link)  #Page refreshes to show response/result
    else:
        return redirect('/')
    
# @app.route('/mywebhook')
# def listening_for_events():
#     body = request.get_json()
#     print(body)

#     return jsonify({
#         "status": 200
#         })
    
if __name__== "__main__":
    app.run(debug=True)