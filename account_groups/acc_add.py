from sdk.color_print import c_print
from tqdm import tqdm

def add_account_groups(session, account_groups, logger):
    '''
    Accepts a tenant session and a list of account groups to add.
    Adds all the account groups to the tenant of the supplied session.
    '''
    
    tenant_name = session.tenant

    if account_groups:
        logger.info(f'Adding Account Groups to tenant: \'{tenant_name}\'')
        
        for acc_grp in tqdm(account_groups, desc='Adding Account Groups'):
            logger.debug('API - Adding Account Group')
            session.request('POST', '/cloud/group', json=acc_grp)
    else:
        logger.info(f'No Account Groups to add for tenant: \'{tenant_name}\'')