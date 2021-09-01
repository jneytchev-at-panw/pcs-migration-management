from tqdm import tqdm

def update_accounts(cln_session, accounts_to_update, logger):
    '''
    Updates the details of cloud accounts on the clone tenant
    '''
    if accounts_to_update:
        logger.info(f'Updating Cloud Accounts for tenant \'{cln_session.tenant}\'')

        for account in tqdm(accounts_to_update, desc='Updating Cloud Accounts', leave=False):
            cloud_type = ''
            cld_id = ''

            if 'cloudAccount' in account:
                cloud_type = account['cloudAccount']['cloudType']
                cld_id = account['cloudAccount']['accountId']
            else:
                cloud_type = account['cloudType']
                cld_id = account['accountId']

            #Patch children of orgs
            if 'cloudAccount' in account:
                if 'parentId' in account['cloudAccount']:
                    if account['cloudAccount']['parentId'] != None:
                        patch = {
                            "groupIds": account['cloudAccount']['groupIds']
                        }
                        status = account['cloudAccount']['enabled']
                        if status == True:
                            status = 'true'
                        if status == False:
                            status = 'false'

                        logger.debug('API - Patching child account')
                        cln_session.request('PATCH', f'/cloud/{cloud_type}/{cld_id}', json=patch)
                        cln_session.request('PATCH', f'/cloud/{cld_id}/status/{status}')
                    else:
                        #Update cloud account
                        logger.debug('API - Updating cloud account')
                        cln_session.request('PUT', f'/cloud/{cloud_type}/{cld_id}', json=account)
                else:
                    #Update cloud account
                    logger.debug('API - Updating cloud account')
                    cln_session.request('PUT', f'/cloud/{cloud_type}/{cld_id}', json=account)
            else:
                #Update cloud account
                logger.debug('API - Updating cloud account')
                cln_session.request('PUT', f'/cloud/{cloud_type}/{cld_id}', json=account)
    else:
        logger.info(f'No Cloud Accounts to update for tenant \'{cln_session.tenant}\'')