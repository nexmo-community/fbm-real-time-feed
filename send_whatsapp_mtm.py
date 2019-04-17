import jwt # https://github.com/jpadilla/pyjwt -- pip3 install PyJWT
import time
import json
import requests
from uuid import uuid4

# NOTE: You will have to replace the Nexmo template info with your own business template info
def send_whatsapp_template (sender, recipient):

    expiry = 1*60*60 # JWT expires after one hour (default is 15 minutes)
    
    f = open(filename, 'r')
    private_key = f.read()
    f.close()
    
    data_body = json.dumps({
        "from":{
            "type":"whatsapp",
            "number": sender
        },
        "to":{
            "type":"whatsapp",
            "number": recipient
        },
        "message":{
            "content":{
                "type":"template",
                "template":{
                    "name":"whatsapp:hsm:technology:nexmo:verify",
                    "parameters":[
                        {
                            "default":"Nexmo Verification"
                        },
                        {
                            "default":"64873"
                        },
                        {
                            "default":"10"
                        }
                    ]
                }
            }
        }
    })

    payload = {
        'application_id': app_id,
        'iat': int(time.time()),
        'jti': str(uuid4()),
        'exp': int(time.time()) + expiry,
    }

    gen_jwt  = jwt.encode(payload, private_key, algorithm='RS256')
    auth = b'Bearer '+gen_jwt
    headers = {'Authorization': auth, 'Content-Type': 'application/json'}
    r = requests.post('https://api.nexmo.com/v0.1/messages', headers=headers, data=data_body)
    return r.json()
