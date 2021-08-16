from sdk.color_print import c_print

def get_requirement_id_by_name(session, standard_id, name):
    '''
    Accepts a tenant session object, a compliance standard ID, and the name of a requirement.

    This is a helper function for compliance syncing. Using the name of a
    requirement and the standard ID the requirement belongs to, gets the requirement ID.
    '''

    c_print('API - Getting requirement by name')
    res = session.request('GET', f'/compliance/{standard_id}/requirement')
    data = res.json()
    for req in data:
        if req['name'] == name:
            return req['id']
    return 'BAD'

#==============================================================================

def get_compliance_standard_id_by_name(session, name):
    '''
    Accepts a tenant session object, a compliance standard ID, and the name of a requirement.

    This is a helper function for compliance syncing. Using the name of a
    standard, the standards ID will be returned..
    '''

    c_print('API - Getting compliance standard by name')
    res = session.request('GET', '/compliance')
    data = res.json()

    for cmp in data:
        if cmp['name'] == name:
            return cmp['id']
    return 'BAD'

#==============================================================================

def get_compliance_standard_list(session: object, logging: bool=False):
    '''
    Accepts a tenant session object and an optional logging flag.

    Gets the list of compliance standards from the tenant.
    '''

    endpoint_url = '/compliance'

    c_print(f'API - Get compliance standard list from tenant \'{session.tenant}\'')
    res = session.request('GET', endpoint_url)

    compliance_standards = dict()
    if res.status_code == 200:
        compliance_standards = res.json()
        c_print(f'Got {len(compliance_standards)} compliance standards from tenant: \'{session.tenant}\'')
        print()

    if logging:
        for el in compliance_standards:
            print(el)
            print()

    return compliance_standards

#==============================================================================

def get_compliance_requirement_list(session: object, standard: dict, logging: bool=False):
    '''
    Accepts a tenant session object, the compliance standard, and an optional logging flag.

    Gets the requirements standards lists from the supplied standard.
    '''

    #Needs a standard object not just an ID so the name of the standard can printed out. 
    std_id = standard['id']
    std_name = standard['name']
    c_print(f'API - Get compliance requirements from tenant \'{session.tenant}\'')
    res = session.request('GET', f'/compliance/{std_id}/requirement')

    requirements = dict()
    if res.status_code == 200:
        requirements = res.json()
        c_print(f'Got {len(requirements)} requirements from standard \'{std_name}\'', color='green')
        print()

    if logging:
        for el in requirements:
            print(el)
            print()

    return requirements

#==============================================================================

def get_compliance_sections_list(session: object, requirement: dict, logging: bool=False):
    '''
    Accepts a tenant session object, the compliance requirement, and an optional logging flag.

    Gets the list of compliance sections from the supplied compliance requirement.
    '''
    
    #Needs a requirement object not just an ID so the name of the requirement can be printed out.
    req_id = requirement['id']
    req_name = requirement['name']

    c_print(f'API - Get compliance section from tenant \'{session.tenant}\'')
    res = session.request('GET', f'/compliance/{req_id}/section')

    sections = dict()
    if res.status_code == 200:
        sections = res.json()
        c_print(f'Got {len(sections)} sections from requirement \'{req_name}\'', color='green')
        print()

    if logging:
        for el in sections:
            print(el)
            print()
    
    return sections

#==============================================================================
#Test code
if __name__ == '__main__':
    from sdk.load_config import load_config_create_sessions

    tenant_sessions = load_config_create_sessions()

    get_compliance_standard_list(tenant_sessions[0], True)