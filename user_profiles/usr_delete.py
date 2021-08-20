import requests

from sdk.color_print import c_print

def delete_user_profiles(session, users):
    if users:
        c_print(f'Deleteing User Profiles from tenant: \'{session.tenant}\'', color='blue')
        print()

        for user in users:
            #The email address that is used as the ID in the URL must be encoded. 
            encoded_id = requests.utils.quote(user['email'])

            print('API - Deleting User Profiles')
            session.request('DELETE', f'/user/{encoded_id}')
    else:
        c_print(f'No User Profiles to delete for tenant: \'{session.tenant}\'', color='yellow')
        print()
