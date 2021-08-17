from sdk.color_print import c_print

def get_all_network_settings(session: object):
    params = {'type':'Network'}
    c_print('API - Getting all anomaly settings')
    res = session.request('GET', '/anomalies/settings', params=params)
    data = res.json()

    return data

def get_all_ueba_settings(session: object):
    params = {'type':'UEBA'}
    c_print('API - Getting all anomaly settings')
    res = session.request('GET', '/anomalies/settings', params=params)
    data = res.json()

    return data

def get_setting(session: object, plc_id: str):
    c_print('API - Getting anomaly setting')
    res = session.request('GET', f'/anomalies/settings/{plc_id}')
    data = res.json()
    
    return data

def get_trusted_lists(session: object):
    c_print('API - Getting anomaly trusted list')
    res = session.request('GET', '/anomalies/trusted_list')
    data = res.json()

    return data

if __name__ == '__main__':
    from sdk.load_config import load_config_create_sessions
    tenant_sessions = load_config_create_sessions()
    
    data = get_all_network_settings(tenant_sessions[0])

    print(data)
    print()
    for el in data:
        print(el)
        res = get_setting(tenant_sessions[0], el)
        print(res)