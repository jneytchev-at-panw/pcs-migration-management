import requests
from sdk.color_print import c_print

def update_user_profiles(session, users):
    if users:
        c_print(f'Updating User Profiles on tenant: \'{session.tenant}\'', color='green')
        print()

        for user in users:
            #The email address that is used as the ID in the URL must be encoded. 
            encoded_id = requests.utils.quote(user['email'])
            
            print('API - Updating User Profile')
            session.request('PUT', f'/v2/user/{encoded_id}', user)

    else:
        c_print(f'No User Profiles to update for tenant: \'{session.tenant}\'',color='yellow')
        print()