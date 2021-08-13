#compares the tenants to find the missing user/s
from sdk.color_print import c_print

#FIXME
def compare_users(source_users: list, clone_users: list, clone_roles: list):
    users_to_add = []
    for src_usr in source_users:
        # check whether if the key 'email' values are in both src_user and dst_user
        if src_usr['email'] not in [cln_user['email'] for cln_user in clone_users]:
            
            #Translate the UUIDs of the roles
            for index in range(len(src_usr['roles'])):
                for cln_role in clone_roles:
                    if src_usr['roles'][index].get('name') == cln_role.get('name'):
                        src_usr['roles'][index].update(id=cln_role.get('id'))
                        src_usr['roleIds'][index] = cln_role.get('id')
                        #FIXME NEEDS TO UPDATE DEFAULT ROLEEEE

            users_to_add.append(src_usr)

    return users_to_add