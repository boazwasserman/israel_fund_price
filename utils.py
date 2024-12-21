import ngrok
import os
from pathlib import Path
import logging

def wrap_with_ngrok(port):
    if not os.path.isfile(Path(__file__).parent / '.ngrok_auth'):
        raise Exception("To run with ngrok, a file named .ngrok_auth needs to exist and contain your ngrok authtoken.")
    if not os.path.isfile(Path(__file__).parent / '.ngrok_domain'):
        print("To run with a static ngrok domain, a file named .ngrok_domain needs to exist and contain your ngrok static domain. Such file doesn't exist, so will generate a random, temporary domain.")
        domain_name = None
    else:
        domain_name = open(Path(__file__).parent / '.ngrok_domain', 'r').readline().strip()
    os.environ['NGROK_AUTHTOKEN'] = open(Path(__file__).parent / '.ngrok_auth', 'r').readline().strip()
    logging.basicConfig(level=logging.INFO)
    ngrok.connect(port, authtoken_from_env=True, domain=domain_name)
