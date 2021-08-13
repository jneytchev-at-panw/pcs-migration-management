from sdk import load_config
from sdk.colors import c_print
from users_migrate.users_call import compare_users, call_source, call_destination, temp_source, destination_role

'''
calls the function for comparing the users from both tenants and uploads the missing user/s
to one or more destination.
'''

#session_one and session_two are use to separate the source with the destination.
#if either is used for both the source or destination, the script won't work.
def upload_users(session_one, session_two, dest_session):
    new_user = compare_users(call_source(session_one), call_destination(session_two), temp_source(session_one), destination_role(session_two))

    # checks whether the list is empty
    if len(new_user):
        user_to_add = []
        #appends the parameters required for POST to properly upload the user/s
        for element in new_user:
            payload = {
                "firstName": element["firstName"],
                "lastName": element["lastName"],
                "defaultRoleId": element["defaultRoleId"],
                "displayName": element["displayName"],
                "roleIds": element["roleIds"],
                "timeZone": element["timeZone"],
                "email": element["email"]
            }
            user_to_add.append(payload)

        #iterates through user_to_add and store the data by dictionaries individually
        new_data = []
        for k in range(len(user_to_add)):
            new_data = user_to_add[k]

            response = session_two.request("POST", "/v2/user", json=new_data)
            if response.status_code == 200:
                c_print("API - Migrating user account", color='blue')

        return new_data

    #prints the following string if the list is empty (no data to compare when both tenants users are the same)
    else:
        c_print("\nNo Data to Migrate!", color='yellow')
        print()

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    #checks whether there are more than one destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            upload_users(tenant_sessions[0], tenant_sessions[index], tenant_sessions[index])