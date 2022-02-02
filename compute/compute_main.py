import compute
from sdk.load_config import load_config_create_sessions
from compute import compute_session_manager
from loguru import logger
import requests

def run():
    tenant_sessions = load_config_create_sessions(True, logger)

    compute_sessions = compute_session_manager.create_sessions(tenant_sessions)

    res = compute_sessions[0].request('GET', 'api/v1/groups')
    print(res.json())
