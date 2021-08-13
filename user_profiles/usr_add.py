from sdk.color_print import c_print

def add_users(session: object, users_to_add: list):
    '''
    Accepts a tenant session object and a list of users to add.

    Adds each user in the list to the tenant of the provided tenant session.
    The User Profiles in the users_to_add list have to have already had their Role IDs
    translated before running this function.
    '''
    tenant_name = session.tenant
    # checks whether the list is empty
    if users_to_add:
        print(f'Adding User Profiles to tenant: \'{tenant_name}\'')
        print()
        
        user_to_add = []
        #iterates through user_to_add and store the data by dictionaries individually
        for user in users_to_add:
            #The role IDs of each user were translated in the compare potion of the code
            print('API - Adding User Profile')
            res = session.request("POST", "/v2/user", json=user)


    #prints the following string if the list is empty
    else:
        c_print(f'No User Profiles to add for tenant: \'{tenant_name}\'', color='yellow')
        print()
