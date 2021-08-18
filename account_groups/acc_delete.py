from sdk.color_print import c_print

def delete_account_groups(session, account_groups):
    if account_groups:
        c_print(f'Deleting Account Groups for tenant: \'{session.tenant}\'',color='blue')
        print()

        for acc in account_groups:
            grp_id = acc.get('id')
            print('API - Deleteing Account Group')
            session.request('DELETE', f"/cloud/group/{grp_id}")

    else:
        c_print(f'No Account Groups to delete for tenant: \'{session.tenant}\'', color='yellow')
        print()