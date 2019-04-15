import jwt # https://github.com/jpadilla/pyjwt -- pip3 install PyJWT
import time
import json
import requests
from uuid import uuid4
from pprint import pprint

class Client:

    expiry = 1*60*60 # JWT expires after one hour (default is 15 minutes)

    def __init__(self, app_id, filename):
        
        f = open(filename, 'r')
        self.private_key = f.read()
        f.close()

        self.app_id = app_id
        
        return

    def send_message (self, channel_type, sender, recipient, msg):
        
        print("Sending message via [%s]-> from: %s to: %s msg: %s" % (channel_type, sender, recipient, msg))

        if channel_type == 'messenger':
            from_field = "id"
            to_field = "id"
        elif channel_type == 'whatsapp' or channel_type == "sms": 
            from_field = "number"
            to_field = "number"
        elif channel_type == 'viber_service_msg':
            from_field = "id"
            to_field = "number"
               
        data_body = json.dumps({
            "from": {
	        "type": channel_type,
	        from_field: sender
            },
            "to": {
	        "type": channel_type,
	        to_field: recipient
            },
            "message": {
	        "content": {
	            "type": "text",
	            "text": msg
	        }
            }
        })

        self.payload = {
            'application_id': self.app_id,
            'iat': int(time.time()),
            'jti': str(uuid4()),
            'exp': int(time.time()) + self.expiry,
        }

        gen_jwt  = jwt.encode(self.payload, self.private_key, algorithm='RS256')
        auth = b'Bearer '+gen_jwt
        headers = {'Authorization': auth, 'Content-Type': 'application/json'}
        r = requests.post('https://api.nexmo.com/v0.1/messages', headers=headers, data=data_body)
        j = r.json()
        pprint(j)
        return
