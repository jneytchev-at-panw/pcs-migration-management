from sdk.color_print import c_print

def api_get_custom(tenant: object, logging: bool=False):
    '''
    Accepts a tenant session object and a logging flag.

    Gets custom policies from the tenant.
    '''
    endpoint_url = '/v2/policy'
    params = {"policy.policyMode":"custom"}

    res = tenant.request('GET', endpoint_url, params=params)

    c_print(f'Got {len(res.json())} custom policies.\n', color='green')

    policies = res.json()

    if logging:
        for policy in policies:
            c_print(policy['name'], color='green')
            print(policy)
            print()
    
    return policies

#==============================================================================

def api_get_default(tenant: object, logging: bool=False):
    endpoint_url = '/v2/policy'
    params = {"policy.policyMode":"redlock_default"}

    res = tenant.request('GET', endpoint_url, params=params)

    c_print(f'Got {len(res.json())} default policies.\n', color='green')

    policies = res.json()

    if logging:
        for policy in policies:
            c_print(policy['name'], color='green')
            print(policy)
            print()
    
    return policies

#==============================================================================

if __name__ == '__main__':
    from sdk import load_config

    tenant_sessions = load_config.load_config_create_sessions()

    api_get_custom(tenant_sessions[0], True)
    # api_get_default(tenant_sessions[0])