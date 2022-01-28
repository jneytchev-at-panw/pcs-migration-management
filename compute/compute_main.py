import compute
from sdk.load_config import load_config_create_sessions
from loguru import logger
import requests

def run():
    tenant_sessions = load_config_create_sessions(True, logger)


    session = tenant_sessions[0]

    res = session.request('GET', 'meta_info')

    print(res.json()['twistlockUrl'])
    compute_url = res.json()['twistlockUrl']
    compute_url += '/api/v1/authenticate'

    compute_session = requests.request('POST', compute_url, json={"username":None,"password":None,"token":session.token})

    compute_token = compute_session.json()['token']

    print(compute_token)
