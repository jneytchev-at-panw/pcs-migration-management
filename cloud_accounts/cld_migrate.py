from cloud_accounts import cld_get, cld_add, cld_keys, cld_compare
from sdk.color_print import c_print

def migrate(tenant_sessions: list):
    '''
    Accepts a list of tenant session objects.

    Migrates all cloud accounts from the first tenant, (source tenant)
    to all other tenants (clone tenants).
    '''

    #Get all cloud accounts names from both tenants
    tenant_cloud_account_names = []
    for i in range(len(tenant_sessions)):
        accounts = cld_get.get_names(tenant_sessions[i])
        tenant_cloud_account_names.append(accounts)

    #Get private cloud keys from user
    gcp_account_keys = cld_keys.get_gcp_credentials(tenant_cloud_account_names[0])
    azure_account_keys = cld_keys.get_azure_credentials(tenant_cloud_account_names[0])

    #Compare cloud accounts to determine which accounts to add to new tenant
    tenant_cloud_accounts_to_add = cld_compare.get_accounts_to_add(tenant_sessions, tenant_cloud_account_names)

    #Get additional info about the cloud accounts missing from the clones from the original tenant.
    clone_tenants_cloud_accounts_to_upload = []
    for i in range(len(tenant_cloud_accounts_to_add)):
        cloud_accounts_to_upload = []
        for j in range(len(tenant_cloud_accounts_to_add[i])):
            account = tenant_cloud_accounts_to_add[i][j]
            ret = cld_get.get_info(tenant_sessions[0], account)#get cloud account info from original tenant
            if ret != '':
                cloud_accounts_to_upload.append(ret)
        clone_tenants_cloud_accounts_to_upload.append(cloud_accounts_to_upload)

    #Upload cloud accounts missing from each tenant
    for i in range(len(clone_tenants_cloud_accounts_to_upload)):
        cld_add.add_accounts(tenant_sessions[i+1], clone_tenants_cloud_accounts_to_upload[i],
                                              azure_account_keys, gcp_account_keys)

    c_print('Finished migrating Cloud Accounts', color='blue')
    print()

if __name__ == '__main__':
    from sdk import load_config
    
    #Generate a API session for each tenant
    tenant_sessions = load_config.load_config_create_sessions()
    
    migrate(tenant_sessions)