def get_names(session: object):
    '''
    Gets a list of all the cloud accounts and their names on a tenant.
    '''

    querystring = {'excludeAccountGroupDetails': 0 }

    print(f'API - Gettings cloud account names from tenant: {session.tenant}.')
    response = session.request('GET', '/cloud/name', params=querystring)

    data = response.json()

    accounts_found = len(data)

    print(f'Got {accounts_found} accounts from tenant: {session.tenant}.')
    print()

    return data