from sdk.color_print import c_print

def update_accounts(cln_session, accounts_to_update):
    '''
    Updates the details of cloud accounts on the clone tenant
    '''
    if accounts_to_update:
        c_print(f'Updating Cloud Accounts for tenant \'{cln_session.tenant}\'', color='blue')
        print()

        for account in accounts_to_update:
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

                        print('API - Patching child account')
                        cln_session.request('PATCH', f'/cloud/{cloud_type}/{cld_id}', json=patch)
                        cln_session.request('PATCH', f'/cloud/{cld_id}/status/{status}')
                    else:
                        #Update cloud account
                        c_print('API - Updating cloud account')
                        cln_session.request('PUT', f'/cloud/{cloud_type}/{cld_id}', json=account)
                else:
                    #Update cloud account
                    c_print('API - Updating cloud account')
                    cln_session.request('PUT', f'/cloud/{cloud_type}/{cld_id}', json=account)
            else:
                #Update cloud account
                c_print('API - Updating cloud account')
                cln_session.request('PUT', f'/cloud/{cloud_type}/{cld_id}', json=account)
    else:
        c_print(f'No Cloud Accounts to update for tenant \'{cln_session.tenant}\'', color='yellow')