import sys
from Client.Client import Client

if len(sys.argv) < 4:
    print('Usage: test-viber.py app_id viber_id to_phone')
    exit(-1)

client = Client(sys.argv[1], "viber.key")
client.send_message('viber_service_msg', sys.argv[2], sys.argv[3], 'Hello from generic client')

