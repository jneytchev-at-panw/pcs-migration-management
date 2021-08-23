from sdk.color_print import c_print

def delete_policies(session, policies):
    if policies:
        c_print(f'Deleteing Policies from tenant \'{session.tenant}\'', color='green')
        print()

        for policy in policies:
            plc_id = policy['policyId']
            name = policy['name']
            print(f'API - Deleting policy \'{name}\'')
            session.request('DELETE', f'/policy/{plc_id}', status_ignore=[204])
    else:
        c_print(f'No Policies to delete from tenant \'{session.tenant}\'', color='yellow')
        print()
