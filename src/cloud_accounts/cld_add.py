from sdk.color_print import c_print

def add_accounts(session: object, accounts: list, azure_account_keys: dict,
                    gcp_account_keys: dict) -> bool:

    #List of redlock errors to manually handle and have ignored by session.request
    redlock_ignore = ['not_account_owner', 'project_id_credential_mismatch', 'data_security_not_enabled_for_tenant', 'organization_viewer_permission_required', 'project_viewer_permission_required']

    tenant_name = session.tenant

    if accounts:
        print('Adding Cloud Accounts to tenant: \'{}\'')
        print()
        for account in accounts:
            res = object()
            cloud_type = ''
            account_type = ''
            account_name = ''
            account_id = ''

            #Correctly set variables
            if 'cloudAccount' in account:
                if account['cloudAccount']['parentId'] != None: #Skip children of org accounts
                    continue
                #Set variables
                cloud_type = account['cloudAccount']['cloudType']
                account_name = account['cloudAccount']['name']
                account_id = account['cloudAccount']['accountId']
            else:
                #Set variables
                cloud_type = account['cloudType']
                account_type = account['accountType']
                account_name = account['name']
                account_id = account['accountId']

            if cloud_type == 'aws':
                res = add_aws(session, account, redlock_ignore)
            if cloud_type == 'azure':
                res = add_azure(session, account, azure_account_keys, redlock_ignore)
            if cloud_type == 'gcp':
                res = add_gcp(session, account, gcp_account_keys, redlock_ignore)
            if cloud_type== 'alibaba_cloud':
                res = add_alibaba(session, account, redlock_ignore)

            try:
                if res.status_code != 200:
                    if 'x-redlock-status' in res.headers:
                        if  redlock_ignore[0] in res.headers['x-redlock-status']:
                            c_print('FAILED', color='red')
                            c_print(f'{cloud_type} cloud account {account_name}::{account_id} already onboarded to application stack.', color='yellow')
                            c_print('not_account_owner', color='red')
                            print()
                        if redlock_ignore[1] in res.headers['x-redlock-status']:
                            c_print('FAILED', color='red')
                            c_print(f'Incorrect or invalid credentials for {cloud_type} account {account_name}::{account_id}.', color='yellow')
                            c_print('project_id_credential_mismatch', color='red')
                            print()
                        if redlock_ignore[2] in res.headers['x-redlock-status']:
                            c_print('FAILED', color='red')
                            c_print('Data security not enabled on this tenant', color='yellow')
                            c_print('data_security_not_enabled_for_tenant', color='red')
                            print()
                        if redlock_ignore[3] in res.headers['x-redlock-status']:
                            c_print('FAILED', color='red')
                            c_print('Problem with GCP Organization Key - No viewer permission', color='yellow')
                            c_print('organization_viewer_permission_required', color='red')
                            print()
                        if redlock_ignore[4] in res.headers['x-redlock-status']:
                            c_print('FAILED', color='red')
                            c_print('Problem with GCP Project Key - No viewer permission', color='yellow')
                            c_print('organization_viewer_permission_required', color='red')
                            print()
            except:
                c_print(account, color='red')
    else:
        c_print('No Cloud Accounts to add for tenant: \'{}\'', color='yellow')
        print()
        

#==============================================================================

def add_aws(session: object, account: dict, redlock_ignore: list=None) -> bool:
    endpoint_url = "/cloud/aws"

    querystring = {"skipStatusChecks":1}

    #Account Groups are not specified here as they do not exists yet.
    if 'groupIds' in account:
        account.update(groupIds=[])
    if 'accountGroupInfos' in account:
        account.update(accountGroupInfos=[])
    if 'defaultAccountGroupId' in account:
        account.pop('defaultAccountGroupId')


    c_print('API - Add AWS account ', account['name'], '::', account['accountId'])
    response = session.request('POST', endpoint_url, json=account, params=querystring, redlock_ignore=redlock_ignore)

    return response

#==============================================================================

def add_azure(session: object, account: dict, azure_keys: dict, redlock_ignore: list=None) -> bool:
    if account['cloudAccount']['accountId'] in azure_keys:
        account.update(key=azure_keys[account['cloudAccount']['accountId']])

    account['cloudAccount'].update(groupIds=[])

    #Account Groups are not specified here as they do not exists yet.
    if 'groupIds' in account['cloudAccount']:
        account['cloudAccount'].update(groupIds=[])
    if 'accountGroupInfos' in account['cloudAccount']:
        account['cloudAccount'].update(accountGroupInfos=[])
    if 'defaultAccountGroupId' in account:
        account.pop('defaultAccountGroupId')

    
    querystring = {"skipStatusChecks":1}

    c_print('API - Add Azure Account: ', account['cloudAccount']['name'], '::', account['cloudAccount']['accountId'])
    response = session.request("POST", '/cloud/azure', json=account, params=querystring, redlock_ignore=redlock_ignore)
    
    return response

#==============================================================================

def add_gcp(session: object, account: dict, gcp_keys: dict, redlock_ignore: list=None):
    endpoint_url = "/cloud/gcp"

    querystring = {"skipStatusChecks":1}

    accountId = account['cloudAccount']['accountId']

    if accountId in gcp_keys:
        account['credentials'].update(private_key=gcp_keys[accountId]['private_key']) 
        account['credentials'].update(private_key_id=gcp_keys[accountId]['private_key_id'])

    account['cloudAccount'].update(enabled=False)#FIXME

    #Account Groups are not specified here as they do not exists yet.
    if 'groupIds' in account['cloudAccount']:
        account['cloudAccount'].update(groupIds=[])
    if 'accountGroupInfos' in account['cloudAccount']:
        account['cloudAccount'].update(accountGroupInfos=[])
    if 'defaultAccountGroupId' in account:
        account.pop('defaultAccountGroupId')
    
    c_print('API - Add GCP Account: ', account['cloudAccount']['name'], '::', account['cloudAccount']['accountId'])
    response = session.request("POST", endpoint_url, json=account, params=querystring, redlock_ignore=redlock_ignore)

    return response

#==============================================================================

def add_alibaba(session: object, account: dict, redlock_ignore: list=None) -> bool:
    endpoint_url = "/cloud/alibaba_cloud"

    querystring = {"skipStatusChecks":1}

    account.update(groupIds=[])

    c_print('API - Add Alibaba Account: ', account['name'], '::', account['accountId'])
    response = session.request('POST', endpoint_url, params=querystring, json=account, redlock_ignore=redlock_ignore)

    return response

#==============================================================================

def add_oci(token: str, api_url, account: dict, redlock_ignore: list=None) -> bool:
    pass
