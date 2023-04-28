from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
import uuid
import requests


app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})

#Printing details of available banks in the country 
'''
response = requests.get('https://api.paystack.co/bank', 
                        params={
                            'country':'nigeria',
                            "pay_with_bank" : True
                        },
                        )
banks = response.json()
for bank_details in banks['data']:
    print(f'{bank_details}\n')
'''
#Validating your bank acount
'''
response = requests.get('https://api.paystack.co/bank/resolve', 
                        params={
                            'account_number':'2230914852',
                            'bank_code': '033'
                        },
                        headers = {
                            'Authorization': 'Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404'
                            },
                        )
'''
#Creating a transfer recipient
'''
response = requests.post('https://api.paystack.co/transferrecipient', 
                        headers = {
                            'Authorization': 'Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404',
                            'Content-Type': 'application/json'
                            },
                        json = {"type": "nuban",
                            "name": "T",
                            "account_number": "0233552560",
                            "bank_code": "058",
                            "currency": "NGN"
                            },
                        )
ref = uuid.uuid4()
'''

#Initiate a transfer
'''
reference = uuid.uuid4()

response = requests.post ('https://api.paystack.co/transfer',
                            headers = {
                                "Authorization": "Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404",
                                "Content-Type": "application/json"
                            },
                            json = {
                                "source": "balance",
                                "reason": "Calm down", 
                                "amount": "3794800", 
                                "reference": f'{reference}',
                                "recipient": "RCP_gx2wn530m0i3w3m"
                                }               
                            )
'''

#Initialize Transaction
'''
email = "jhimmie.jimi@gmail.com"
amount = 800
response = requests.post(
                        "https://api.paystack.co/transaction/initialize",
                        headers={
                            'Authorization': 'Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404',
                            'Content-Type': 'application/json'
                            },
                        json={
                            "email": email,
                            "amount": amount*100
                        }
                    )
'''
#Verify Transaction
'''
reference = 'zu8nmyev66'
response = requests.get(
                       f"https://api.paystack.co/transfer/verify/{reference}",
                       headers={
                           "Authorization" : "Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404",  
                       } 
                )
'''
'''response = requests.get(
                       f"https://api.paystack.co/transaction/2609111127",
                       headers={
                           "Authorization" : "Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404",  
                       } 
                    )
details = response.json()
for k, val  in details['data'].items():
    print("-------------------------------------")
    print(f"{k} {val} \n")
    # for a, b in value.items():
    #     print(f"{a} : {b} \n")
    # print("-------------------------------------")

# '''
        
# print(details)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/verify", methods=['GET','POST'])
def resolve_account():
    if request.method == 'POST':
        account_number = request.form.get('account_number')
        bank_code = request.form.get('bank_code')

        response = requests.get('https://api.paystack.co/bank/resolve', 
                            params={
                                'account_number': f'{account_number}',
                                'bank_code': f'{bank_code}'
                            },
                            headers = {
                                'Authorization': 'Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404'
                                },
                            )
        data = response.json()
        print(data)
        return render_template('index.html', r_account=data)
    else:
        return redirect('/')


@app.route("/create_recipient", methods=['GET','POST'])
def create_transfer_recipient():
    if request.method == 'POST':
        print(request.form)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        account_number = request.form.get('account_number')
        bank_code = request.form.get('bank_code')
        account_type =  request.form.get('type')
        currency = request.form.get('currency')

        response = requests.post('https://api.paystack.co/transferrecipient', 
                        headers = {
                            'Authorization': 'Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404',
                            'Content-Type': 'application/json'
                            },
                        json = {"type": account_type,
                            "name": f'{first_name} {last_name}',
                            "account_number": account_number,
                            "bank_code": bank_code,
                            "currency": currency
                            },
                        )
        data = response.json()
        print(data)
        return render_template('index.html', t_recipient=data)
    else:
        return redirect('/')

@app.route("/get_banks", methods=['GET','POST'])
def get_bank_list():
    if request.method == 'POST':
        country = f"{request.form.get('country')}"
        print(country)
        response = requests.get('https://api.paystack.co/bank', 
                        params={
                            'country':country.lower()
                        },
                        )
        
        data = response.json()
        print(data)
        return render_template('index.html', banks=data)
    else:
        return redirect('/')

@app.route('/transaction/initialize', methods=["GET", "POST"])
def initialize_transaction():
    email = "toluwalope.david@gmail.com"
    amount = 200
    response = requests.post(
                            "https://api.paystack.co/transaction/initialize",
                            headers={
                                'Authorization': 'Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404',
                                'Content-Type': 'application/json'
                                },
                            json={
                                "email": email,
                                "amount": amount*100
                            }
                        )
    return jsonify({200})

# @app.route('/create_charge')
# def create_charge():
response = requests.post(
                            "https://api.paystack.co/transaction/initialize",
                            headers={
                                'Authorization': 'Bearer sk_test_6be99f95d69d234aa607b16ec613208f0b9e6404',
                                'Content-Type': 'application/json'
                                },
                            json={
                                "email" : "jhimmie.jimi@gmail.com",
                                "amount": 1000,
                                "bank": {
                                    "code": "033",
                                    "account_number": "2230914852"
                                }
                            }
                        )
print(response.json())
    
    
@app.route('/mywebhook')
def listening_for_events():
    body = request.get_json()
    print(body)

    return jsonify({
        "status": 200
        })
    
if __name__== "__main__":
    app.run(debug=True)