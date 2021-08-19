from sdk.color_print import c_print

def delete_accounts(cln_session, accounts):
    if accounts:
        c_print(f'Deleting Cloud Accounts from tenant \'{cln_session.tenant}\'', color='blue')
        print()

        for account in accounts:
            cloud_type = ''
            cld_id = ''
            if 'cloudAccount' in account:
                cloud_type = account['cloudAccount']['cloudType']
                cld_id = account['cloudAccount']['accountId']
            else:
                cloud_type = account['cloudType']
                cld_id = account['accountId']
        
            c_print('API - Deleting cloud account')
            cln_session.request('DELETE', f'/cloud/{cloud_type}/{cld_id}')

    else:
        c_print(f'No Cloud Accounts to delete for tenant \'{cln_session.tenant}\'', color='yellow')