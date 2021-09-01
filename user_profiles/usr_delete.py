import requests
from tqdm import tqdm

def delete_user_profiles(session, users, logger):
    if users:
        logger.info(f'Deleteing User Profiles from tenant: \'{session.tenant}\'')

        for user in tqdm(users, desc='Deleting User Profiles', leave=False):
            #The email address that is used as the ID in the URL must be encoded. 
            encoded_id = requests.utils.quote(user['email'])

            logger.debug('API - Deleting User Profiles')
            session.request('DELETE', f'/user/{encoded_id}')
    else:
        logger.info(f'No User Profiles to delete for tenant: \'{session.tenant}\'')
