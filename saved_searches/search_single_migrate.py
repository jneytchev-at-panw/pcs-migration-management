def single_migrate(tenant_sessions, uuid, logger):
   tenant_saved_searches = [] 
   for session in tenant_sessions:
        logger.debug('API - Getting saved searches for each tenant')
        querystring = {"filter":"saved"}
        res = session.request('GET', '/search/history', params=querystring)
        data = res.json()
        tenant_saved_searches.append(data)

    source_tenant = tenant_saved_searches[0]
    clone_tenants = tenant_saved_searches[1:]

    for src_search in source_tenant:
        print(src_search)

