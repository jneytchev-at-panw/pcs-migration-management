def get_users(session):
    '''
    Accepts a tenant session object.

    Calls the API and gets a list of the User Profiles.
    '''

    print('API - Getting User Profiles')
    res = session.request("GET", "/v2/user")
    users = res.json()

    return users

def get_user_roles(session):
    '''
    Accepts a tenant session object.

    Calls the API and gets the list of User Roles used for
    translating the Role IDs associated with a User Profile.
    '''
    
    print('API - Getting User Roles')
    res = session.request("GET", "/user/role")
    roles = res.json()

    return roles
