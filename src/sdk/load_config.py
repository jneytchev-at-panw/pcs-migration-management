import yaml
from sdk.session_manager import Session

def load_config_create_sessions():
    '''
    Reads config.yml and generates a list of tenants and tokens for those tenants.

    Returns:
    List with the tenants list and the tokens list that corespond with each tenant.
    '''
    #Open and load config file
    with open("config.yml", "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    #Parse cfg for tenant names and create tokens for each tenant
    tenant_sessions = []
    for tenant in cfg:
        a_key = cfg[tenant]['credentials']['access_key']
        s_key = cfg[tenant]['credentials']['secret_key']
        api_url = cfg[tenant]['api']['api_url']

        tenant_sessions.append(Session(tenant, a_key, s_key, api_url))

    return tenant_sessions