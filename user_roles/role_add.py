from sdk.color_print import c_print
from user_roles import role_translate_id

def add_roles(session, old_session, roles):
    tenant_name = session.tenant
    if roles:
        print(f'Adding User Roles to tenant: \'{tenant_name}\'')
        print()

        #Translate Acc Grp IDs
        c_print('API - Getting source Account Groups')
        src_acc_grps = old_session.request('GET', '/cloud/group').json()
        c_print('API - Getting destination Account Groups')
        dest_acc_grps = session.request('GET', '/cloud/group').json()

        #Translate Resource List IDs
        c_print('API - Getting source Resource Lists')
        src_rsc_lists = old_session.request('GET', '/v1/resource_list').json()
        c_print('API - Getting destination Resource Lists')
        dest_rsc_lists = session.request('GET', '/v1/resource_list').json()

        for role in roles:
            #Translate Acc Grp IDs
            if 'accountGroupIds' in role:
                new_ids = []
                for index in range(len(role['accountGroupIds'])):
                    old_id = role['accountGroupIds'][index]
                    new_id = role_translate_id.translate_acc_grp_ids(old_id, dest_acc_grps, src_acc_grps)
                    new_ids.append(new_id)
                role.update(accountGroupIds=new_ids)

            #Translate resource List IDS
            if 'resourceListIds' in role:
                new_ids = []
                for index in range(len(role['resourceListIds'])):
                    old_id = role['resourceListIds'][index]
                    new_id = role_translate_id.translate_rsc_list_ids(old_id, dest_rsc_lists, src_rsc_lists)
                    new_ids.append(new_id)
                role.update(resourceListIds=new_ids)

            name = role['name']
            c_print(f'API - Adding role: {name}')
            session.request('POST', '/user/role', json=role)

    else:
        print(f'No User Roles to add for tenant: \'{tenant_name}\'')
        print()