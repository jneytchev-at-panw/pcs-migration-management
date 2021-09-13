if __name__ == '__main__':
    from sdk.load_config import load_config_create_sessions
    from loguru import logger
    tenant_sessions = load_config_create_sessions(True, logger)


    #Check if DS is enabled
    res = tenant_sessions[0].request('GET', '/api/v1/provision/dlp/status')
    print(res.json())

    #Enabled DS
    res = tenant_sessions[1].request('GET', 'api/v1/provision/dlp')
    print(res.json())
    
    