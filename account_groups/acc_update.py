from sdk.color_print import c_print

def update_account_groups(session, account_groups):
    if account_groups:
        c_print(f'Updating Account Groups for tenant: \'{session.tenant}\'', color='green')
        print()

        for acc in account_groups:
            payload = {
                'name': acc.get('name'),
                'description': acc.get('description', ''),
                'accountIds': acc.get('accountIds', [])#,
                #'nonOnboardedCloudAccountIds': acc.get('nonOnboardedCloudAccountIds', []) 
            }
            grp_id = acc.get('id')
            print('API - Updating Account Group')
            session.request('PUT', f"/cloud/group/{grp_id}", json=payload)

    else:
        c_print(f'No Account Groups to update for tenant: \'{session.tenant}\'', color='yellow')
        print()