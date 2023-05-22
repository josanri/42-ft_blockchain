import functools
import hashlib
import datetime
from flask import Flask
from flask import jsonify
from flask import request
from threading import Lock

app = Flask(__name__)
# Run with python -m flask --app .\ft_blockchain.py run

blockchain = []
current_block = None
wallet = 0
lock = Lock()

def calculate_new_proof_of_work():
    
    if len(blockchain) == 0:
        previous_hash = bytes(0)
    else:
        previous_hash = blockchain[-1]["previous_hash"].encode()
    
    end = False
    index = 0
    while not end:
        m = hashlib.sha256()
        m.update(previous_hash)
        m.update(bytes(index))
        new_hash = m.hexdigest()
        if new_hash[-4::] == "4242":
            end = True
        else:
            index += 1
    
    return (new_hash, index)

def generate_new_block():
    block = {
        "index": len(blockchain),
        "timestamp": datetime.datetime.now().timestamp(),
        "transactions": [],
        # "proof": None,
        # "previous_hash": None
    }
    return block

def generate_new_transaction(sender: str, recipient:str, amount: int):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
    }
    return transaction

@app.route('/mine', methods=['GET'])
def get_mine():
    global lock
    global current_block
    global wallet

    if current_block == None or len(current_block["transactions"]) == 0:
        return "Cannot mine if the block has no transactions"
    lock.acquire()
    new_hash, proof = calculate_new_proof_of_work()
    current_block["proof"] = proof
    current_block["previous_hash"] = new_hash
    wallet += sum(transaction["amount"] for transaction in current_block["transactions"]) * 0.01
    map(lambda a: a["amount"] * 0.99, current_block["transactions"]) 
    lock.release()
    blockchain.append(current_block)
    current_block = None
    print("Mined")
    return 'Mine'

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain)

@app.route('/transactions/new', methods=['POST'])
def post_transactions_new():
    global current_block
    if current_block == None:
        current_block = generate_new_block()
    try:
        sender = request.form['sender']
        recipient = request.form['recipient']
        amount = int(request.form['amount'])
        print(type(amount))
        current_block['transactions'].append(generate_new_transaction(sender, recipient, amount))
        return f"New Transaction Done - Sender:{sender}; Recipient: {recipient}; Amount: {amount}"
    except Exception:
        return "Could not process the new transaction"
