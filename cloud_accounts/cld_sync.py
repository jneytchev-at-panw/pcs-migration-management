from sdk.color_print import c_print
from cloud_accounts import cld_migrate, cld_get, cld_compare, cld_update, cld_delete

def sync_cloud_accounts(tenant_sessions: list, addMode: bool, upMode: bool, delMode: bool):
    '''Update, add, or delete cloud accounts to normalize all tenants to be the same as the source tenant'''

    if addMode:
        #Migrate missing cloud accounts first using migrate module
        cld_migrate.migrate(tenant_sessions)

    if upMode or delMode:
        #Get all cloud accounts from both tenants
        tenant_accounts = []
        for i in range(len(tenant_sessions)):
            accounts = cld_get.get_names(tenant_sessions[i])
            tenant_accounts.append(accounts)

        #Get the full information for each cloud account
        tenants_cloud_accounts = []
        for i in range(len(tenant_accounts)):
            cloud_accounts_to_upload = []
            for j in range(len(tenant_accounts[i])):
                account = tenant_accounts[i][j]
                ret = cld_get.get_info(tenant_sessions[i], account)#get info from original tenant
                if ret != '':
                    cloud_accounts_to_upload.append(ret)
            tenants_cloud_accounts.append(cloud_accounts_to_upload)

        #Sync each tenants cloud accounts
        source_tenant_cloud_accounts = tenants_cloud_accounts[0]
        clone_tenants_cloud_accounts = tenants_cloud_accounts[1:]
        cln_tenant_sessions = tenant_sessions[1:]
        for index in range(len(clone_tenants_cloud_accounts)):
            if upMode:
                accounts_to_update = cld_compare.get_accounts_to_update(source_tenant_cloud_accounts, clone_tenants_cloud_accounts[index], tenant_sessions[0], cln_tenant_sessions[index])
                cld_update.update_accounts(cln_tenant_sessions[index], accounts_to_update)
            
            if delMode:
                accounts_to_delete = cld_compare.get_accounts_to_delete(source_tenant_cloud_accounts, clone_tenants_cloud_accounts[index])
                cld_delete.delete_accounts(cln_tenant_sessions[index], accounts_to_delete)


if __name__ == '__main__':
    from sdk import load_config
    
    #Generate a API session for each tenant
    tenant_sessions = load_config.load_config_create_sessions()
    
    sync_cloud_accounts(tenant_sessions, True, True, True)


