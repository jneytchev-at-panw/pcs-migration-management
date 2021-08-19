from sdk.color_print import c_print

def add_resource_lists(session: object, resource_lists_to_add: list):
    tenant_name = session.tenant
    if resource_lists_to_add:
        print(f'Adding Resource Lists to tenant: \'{tenant_name}\'', color='blue')
        print()

        status_ignore = [201]
        for rsc in resource_lists_to_add:
            print('API - Adding Resource List')
            session.request('POST', '/v1/resource_list', json=rsc, status_ignore=status_ignore)

    else:
        
        c_print(f'No Resource Lists to add for tenant: \'{tenant_name}\'', color='yellow')
        print()


