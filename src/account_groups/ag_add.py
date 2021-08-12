from sdk.color_print import c_print


def add_account_groups(session, account_groups):
    '''
    Accepts a tenant session and a list of account groups to add.
    Adds all the account groups to the tenant of the supplied session.
    '''
    if account_groups:
        for acc_grp in account_groups:
            print('API - Adding Account Group')
            session.request('POST', '/cloud/group', json=acc_grp)
    else:
        c_print('No Account Groups to migrate', color='yellow')
        print()