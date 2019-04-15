import sys
from flask import Flask, request, jsonify
from pprint import pprint
from Client.Client import Client

NEXMO_APP_ID = sys.argv[1]
print("Nexmo App ID: %s" % NEXMO_APP_ID)

client = Client(NEXMO_APP_ID, "private.key")
app = Flask(__name__)

@app.route('/inbound', methods=['POST'])
def inbound_message():
    print ("Inbound Message...")    
    data = request.get_json()
    pprint(data)
    return ("inbound_message", 200)

@app.route('/status', methods=['POST'])
def message_status():
    print ("Message status:")    
    data = request.get_json()
    pprint(data)
    return ("message_status", 200)

if __name__ == '__main__':
    app.run(host="localhost", port=9000)

