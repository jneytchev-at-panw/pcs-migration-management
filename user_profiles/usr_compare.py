#compares the tenants to find the missing user/s
from sdk.color_print import c_print

#FIXME
def compare_users(source_users: list, clone_users: list, clone_roles: list):
    users_to_add = []
    for src_usr in source_users:
        # check whether if the key 'email' values are in both src_user and dst_user
        if src_usr['email'] not in [cln_user['email'] for cln_user in clone_users]:

            #Translate the UUID of the roles a user is associated with
            for cln_role in clone_roles:
                for src_role in src_usr['roles']:

                    if src_role['name'] == cln_role['name']:
                        if src_role['id'] != cln_role['id'] :
                            src_usr['roleIds'].append(cln_role['id'])
                            src_role['id'] = cln_role['id']


            # appends the missing values from users_one into users_two
            users_to_add.append(src_usr)

    return users_to_add