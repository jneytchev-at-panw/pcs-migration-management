def get_resource_lists(session: object):
    '''
    Calls the API and gets the list of resource list.
    '''

    print('API - Getting resource lists')
    res = session.request('GET', '/v1/resource_list')
    rsc_lists = res.json()

    return rsc_lists