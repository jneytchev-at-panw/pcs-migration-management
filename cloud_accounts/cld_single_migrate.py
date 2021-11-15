from cloud_accounts import cld_get


def single_migrate(tenant_sessions, uuid, logger):
    tenant_cloud_accounts = [] 
    for session in tenant_sessions:
        cld_account_names = cld_get.get_names(session, logger)

        cld_accounts = []
        for cld in cld_account_names:
            cld_accounts.append(cld_get.get_all_info(session, cld, logger))
        
        tenant_cloud_accounts.append(cld_accounts)
            

        print(cld_accounts)