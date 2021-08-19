from sdk.color_print import c_print
from user_roles import role_add, role_compare, role_get, role_delete, role_update

def sync_roles(tenant_sessions: list, addMode: bool, upMode: bool, delMode: bool):
    #Get roles
    roles_lists = []
    for session in tenant_sessions:
        roles = role_get.get_roles(session)
        roles_lists.append(roles)
    
    clone_tenant_sessions = tenant_sessions[1:]

    if upMode:
        #Get list of roles to update from each tenant
        roles_list_delta_update = role_compare.compare_each_role(roles_lists, tenant_sessions)

        #Updates roles on tenants
        for index, roles in enumerate(roles_list_delta_update):
            session = clone_tenant_sessions[index]
            role_update.update_roles(session, tenant_sessions[0], roles)

    if addMode:
        #Get list of roles to add to each tenant
        roles_list_delta_add = role_compare.compare_added_roles(roles_lists)

        #upload roles to tenants
        for index, roles in enumerate(roles_list_delta_add):
            session = clone_tenant_sessions[index]
            role_add.add_roles(session, tenant_sessions[0], roles)

    if delMode:
        #Get list of roles to delete from each tenant
        roles_list_delta_delete = role_compare.compare_deleted_roles(roles_lists)

        #Delete roles from tenants
        for index, roles in enumerate(roles_list_delta_delete):
            session = clone_tenant_sessions[index]
            role_delete.delete_roles(session, roles)

    c_print('Finished syncing User Roles', color='blue')
    print()

    

if __name__ == '__main__':
    from sdk.load_config import load_config_create_sessions

    tenant_sessions = load_config_create_sessions()
    sync_roles(tenant_sessions, True, True, True)

