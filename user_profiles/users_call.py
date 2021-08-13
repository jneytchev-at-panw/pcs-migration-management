from sdk import load_config
from sdk.colors import c_print

'''
Call request the source and destination tenants and compares
the missing values. If found, append the missing value to a new list.
Replaces the role id with that from the destination in order to 
migrate the user/s without any issues.
'''

def call_source(session, logging=False):
    response = session.request("GET", "/v2/user")
    src_user = response.json()
    #for testing
    if logging:
        c_print(session.tenant, ":", color='yellow')
        for items in src_user:
            print(items)
    return src_user


def call_destination(session, logging=False):
    response = session.request("GET", "/v2/user")
    dst_user = response.json()
    #for testing
    if logging:
        c_print(session.tenant, ":", color='yellow')
        for items in dst_user:
            print(items)
    return dst_user

#a temporary call request for comparing tenants
def temp_source(session):
    response = session.request("GET", "/v2/user")
    data = response.json()
    temp_role_ids = []
    for items in data:
        temp_role_ids.append(items)
    return temp_role_ids

def destination_role(session):
    response = session.request("GET", "/user/role")
    data = response.json()
    dst_role = []
    for item in data:
        dst_role.append(item)
    return dst_role

#compares the tenants to find the missing user/s
def compare_users(src_user: list, dst_user: list, role_ids: list, dst_role: list):
    new_user = []
    for user_in_src in src_user:
        # check whether if the key 'email' values are in both src_user and dst_user
        if user_in_src['email'] not in [key['email'] for key in dst_user]:
            c_print(f"Missing: " + user_in_src.get('firstName'), " ", user_in_src.get('lastName'),
                    ", ", user_in_src.get('email'), color="blue")

            # call request for the user's roles and compares if the roles name in source equals to that of role_id
            for role_id in dst_role:
                for element in user_in_src['roles']:
                    temp_id = element['id']

                    #if 'name' matches for the users and the 'id' does not, appends the correct id, roleIds and
                    #defaultRoleId to migrate the user without errors and without its proper role.
                    if element['name'] == role_id['name']:
                        if element['id'] != role_id['id'] :
                            user_in_src['roleIds'].append(role_id['id'])
                            element['id'] = role_id['id']
                        if user_in_src['defaultRoleId'] == temp_id:
                            user_in_src['defaultRoleId'] = role_id['id']

            #iterates over the roleIds from the destination and compares the old id from the temporary source
            #in order to remove the old ids.
            for ids in role_ids:
                for old_ids in ids['roleIds']:
                    if old_ids in user_in_src['roleIds']:
                        user_in_src['roleIds'].remove(old_ids)

            # appends the missing values from users_one into users_two
            new_user.append(user_in_src)

    return new_user

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    #checks whether there are more than one destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            source = call_source(tenant_sessions[0])
            destination = call_destination(tenant_sessions[index])
            temp_src = temp_source(tenant_sessions[0])
            role_dst = destination_role(tenant_sessions[index])
            compare_users(source, destination, temp_src, role_dst)