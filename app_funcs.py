import sys
from threading import Timer
from Client.Client import Client

# Simulation of our real-time data feed
# Arrays should be of same length
prices = {
    'MSFT': ['120.24', '119.36', '118.34', '119.78', '120.23', '122.98', '140.21', '141.09', '144.98', '155.92', '170.19'],
    'GOOGL': ['1209.24', '1209.66', '1299.54', '1300.19', '1327.26', '1299.12', '1300.00', '11301.91', '1308.67', '1350.11', '1400.01'],
}

users = [] # array of registered users
tic_count = 0

NEXMO_APP_ID = sys.argv[1]
print("Nexmo App ID: %s" % NEXMO_APP_ID)
client = Client(NEXMO_APP_ID, "private.key")

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
    return

def proc_inbound_msg(channel_type, data):

    global nexmo
    global users

    user = {}
    
    if channel_type == "sms":
        msg_text = data['text']
    else:
        msg_text = data['message']['content']['text']

    if channel_type == "messenger":
        user['type'] = channel_type
        user['from'] = data['from']['id']
        user['to'] = data['to']['id']
    elif channel_type == "whatsapp":
        user['type'] = channel_type
        user['from'] = data['from']['number']
        user['to'] = data['to']['number']
    elif channel_type == "sms":
        user['type'] = channel_type
        user['from'] = data['msisdn']
        user['to'] = data['to']        
    else:
        # Viber does not support inbound messages
        print("ERROR: unrecognized channel type")
        
    if 'msft' in msg_text.lower():
        user['symbol'] = "MSFT"
        msg = "Registered for MSFT data."
        users.append(user)
    elif 'googl' in msg_text.lower():
        user['symbol'] = "GOOGL"
        msg = "Registered for GOOGL data."
        users.append(user)
    else:
        msg = "Send us a message with MSFT or GOOGL in it for real-time data."

    client.send_message(user['type'], user['to'], user['from'], msg)
    return

