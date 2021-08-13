from resource_lists import rsc_get, rsc_compare, rsc_add
from sdk.color_print import c_print

def migrate(tenant_sessions: list):
    '''
    Accepts a list of tenant session objects.
    
    Migrates all resource lists from the first tenant, (source tenant)
    to all other tenants (clone tenants).
    '''
    
    #Get all resource lists
    tenant_resource_lists = []
    for session in tenant_sessions:
        data = rsc_get.get_resource_lists(session)
        tenant_resource_lists.append(data)

    #Get resource lists to add
    cln_tenant_rsc_lists_to_add = []
    src_tenant_rsc_lists = tenant_resource_lists[0]
    cln_tenant_rsc_lists = tenant_resource_lists[1:]
    for cln_rsc_lists in cln_tenant_rsc_lists:
        rsc_to_add = rsc_compare.compare_resource_lists(src_tenant_rsc_lists, cln_rsc_lists)
        cln_tenant_rsc_lists_to_add.append(rsc_to_add)

    #Add resource lists
    for index, cln_rsc_lists in enumerate(cln_tenant_rsc_lists_to_add):
        rsc_add.add_resource_lists(tenant_sessions[index + 1], cln_rsc_lists)

    c_print('Finished migrateding Resource Lists', color='blue')
    print()




if __name__ =='__main__':
    from sdk.load_config import load_config_create_sessions

    tenant_sessions = load_config_create_sessions()
    
    migrate(tenant_sessions)