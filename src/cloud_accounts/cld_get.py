def api_get(session: object):
    '''
    Gets a list of all the cloud accounts on a tenant.
    '''
    end_point_url = '/cloud/name'
    querystring = {'excludeAccountGroupDetails': 0 }

    print(f'API - Gettings cloud account names from tenant: {session.tenant}.')
    response = session.request('GET', end_point_url, params=querystring)

    data = response.json()

    accounts_found = len(data)

    print(f'Got {accounts_found} accounts from tenant: {session.tenant}.')
    print()

    return data