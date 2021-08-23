from sdk import load_config, color_print
from policies import plc_get, plc_compare, plc_add, plc_update, plc_migrate_default, plc_delete

def sync(tenant_sessions: list, addMode: bool, upMode: bool, delMode: bool):
    '''
    Adds, updates, and deletes policies from clone tenants until the clone tenants match the source tenant.
    '''
    #Get all custom policies from all tenants
    tenant_custom_policies = []
    for tenant_session in tenant_sessions:
        tenant_custom_policies.append(plc_get.api_get_custom(tenant_session))

    if addMode:
        #Get policies to add
        #Get delta from original tenant policies and clone tenant policies
        policies_to_add = plc_compare.compare_original_to_clones(tenant_sessions, tenant_custom_policies)

        #Upload policies to clone tenants
        clone_tenant_sessions = tenant_sessions[1:]
        for index, policies in enumerate(policies_to_add):
            tenant_session = clone_tenant_sessions[index]
            plc_add.add_custom_policies(tenant_session, tenant_sessions[0], policies)

    if upMode: 
        #Get policies to update
        policies_to_update = plc_compare.get_policies_to_update(tenant_sessions, tenant_custom_policies)

        #Update policies
        for index, policies in enumerate(policies_to_update):
            session = clone_tenant_sessions[index]
            plc_update.update_custom_policies(session, tenant_sessions[0], policies)

    if delMode:
        #Get policies to delete
        policies_to_delete = plc_compare.get_policies_to_delete(tenant_custom_policies)

        #Delete polices
        for index, policies in enumerate(policies_to_delete):
            session = clone_tenant_sessions[index]
            plc_delete.delete_policies(session, policies)

    if upMode:
        #Sync default policy
        plc_migrate_default.migrate_builtin_policies(tenant_sessions)

    color_print.c_print('Finished syncing Policies', color='green')
    print()

if __name__ == '__main__':
    tenant_sessions = load_config.load_config_create_sessions()

    sync(tenant_sessions, True, True, True)
