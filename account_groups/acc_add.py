from sdk.color_print import c_print


def add_account_groups(session, account_groups):
    '''
    Accepts a tenant session and a list of account groups to add.
    Adds all the account groups to the tenant of the supplied session.
    '''
    
    tenant_name = session.tenant

    if account_groups:
        print(f'Adding Account Groups to tenant: \'{tenant_name}\'')
        print()
        
        for acc_grp in account_groups:
            print('API - Adding Account Group')
            session.request('POST', '/cloud/group', json=acc_grp)
    else:
        c_print(f'No Account Groups to add for tenant: \'{tenant_name}\'', color='yellow')
        print()