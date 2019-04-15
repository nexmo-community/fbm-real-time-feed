import sys
from flask import Flask, request, jsonify
from pprint import pprint
from Client.Client import Client
from threading import Timer

NEXMO_APP_ID = sys.argv[1]
print("Nexmo App ID: %s" % NEXMO_APP_ID)

client = Client(NEXMO_APP_ID, "private.key")
app = Flask(__name__)

users = [] # array of registered users

nexmo = {}
nexmo['number'] = sys.argv[2]

# Simulation of our real-time data feed
# Arrays should be of same length
prices = {
    'MSFT': ['120.24', '119.36', '118.34', '119.78', '120.23', '122.98', '140.21', '141.09', '144.98', '155.92', '170.19'],
    'GOOGL': ['1209.24', '1209.66', '1299.54', '1300.19', '1327.26', '1299.12', '1300.00', '11301.91', '1308.67', '1350.11', '1400.01'],
}

tic_count = 0

def update_users():
    print("** update_users **")
    t = Timer(10, update_users)
    t.start()
    global users
    global tic_count

    if tic_count < len(prices['MSFT'])-1: 
        tic_count = tic_count + 1
    else:
        tic_count = 0
    
    for user in users:
        symbol = user['symbol']
        client.send_message(user['type'], user['to'], user['from'], prices[symbol][tic_count])

update_users()

def proc_inbound_msg(data):

    global nexmo
    global users

    user = {}

    channel_type = data['from']['type']
    msg_text = data['message']['content']['text']

    if channel_type == "messenger":
        user['type'] = "messenger"
        user['from'] = data['from']['id']
        user['to'] = data['to']['id']

    if 'MSFT' in msg_text:
        user['symbol'] = "MSFT"
        msg = "Registered for MSFT data."
        users.append(user)
    elif 'GOOGL' in msg_text:
        user['symbol'] = "GOOGL"
        msg = "Registered for GOOGL data."
        users.append(user)
    else:
        msg = "Send us a message with MSFT or GOOGL in it for real-time data."

    client.send_message(user['type'], user['to'], user['from'], msg)
    return

@app.route('/webhooks/inbound', methods=['POST'])
def inbound_message():
    global user
    print ("** inbound_message **")
    proc_inbound_msg(request.get_json())
    return ("inbound_message", 200)

@app.route('/webhooks/status', methods=['POST'])
def message_status():
    print ("** message_status **")
    data = request.get_json()
    pprint(data)
    return ("message_status", 200)

@app.route('/webhooks/inbound-sms', methods=['POST'])
def inbound_sms():
    print ("Inbound SMS:")
    values = request.values
    for k, v in values.items():
        print(k, v)
    user['sms'] = values['msisdn']
    print("User phone: %s" % user['sms'])
    return ("inbound_sms", 200)

@app.route('/webhooks/delivery-receipt', methods=['POST'])
def delivery_receipt():
    print ("Delivery receipt:")
    data = request.get_json()
    pprint(data)
    return ("delivery_receipt", 200)

if __name__ == '__main__':
    app.run(host="localhost", port=9000)

