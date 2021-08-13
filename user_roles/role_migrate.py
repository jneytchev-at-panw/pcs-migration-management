from sdk.color_print import c_print
from user_roles import role_add, role_compare, role_get

def migrate_roles(tenant_sessions: list):
    #Get roles
    roles_lists = []
    for session in tenant_sessions:
        roles = role_get.get_roles(session)
        roles_lists.append(roles)

    #Compare roles
    #FIXME role compare needs to not have the for loop. it should be here
    roles_lists_delta = role_compare.compare_added_roles(roles_lists)

    #upload roles to tenants
    clone_tenant_sessions = tenant_sessions[1:]
    for index, roles in enumerate(roles_lists_delta):
        session = clone_tenant_sessions[index]
        role_add.add_roles(session, tenant_sessions[0], roles)

    c_print('Finished migrating User Roles')
    print()

if __name__ == '__main__':
    from sdk.load_config import load_config_create_sessions

    tenant_sessions = load_config_create_sessions()
    migrate_roles(tenant_sessions)


    