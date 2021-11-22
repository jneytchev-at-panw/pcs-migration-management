from compliance_standards import cmp_add, cmp_get

def single_migrate(tenant_sessions, uuid, logger):
    cmp_type = input('Migrate Compliance Standard, Requirement, or Section. (STD, REQ, SEC): ')

    cmp_type = cmp_type.lower()

    source_session = tenant_sessions[0]

    cmp_to_add = {}

    if cmp_type == 'std':
        res = source_session.request('GET', f'/compliance/{uuid}')
        cmp_to_add = res.json()
    elif cmp_type == 'req':
        res = source_session.request('GET', f'/compliance/requirement/{uuid}')
        cmp_to_add = res.json()
    else:
        #This does not work as its not a valid path
        res = source_session.request('GET', f'/compliance/requirement/section/{uuid}')
        pass


    print(cmp_to_add)