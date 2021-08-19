from sdk.color_print import c_print

def update_resource_lists(session, resource_lists):
    if resource_lists:
        c_print(f'Updating Resource Lists for tenant: \'{session.tenant}\'', color='blue')
        print()

        for rsc_list in resource_lists:
            rl_id = rsc_list['id']
            status_ignore = [201]
            print('API - Updating Resource List')
            session.request("PUT", f"/v1/resource_list/{rl_id}", json=rsc_list, status_ignore=status_ignore)

    else:
        c_print(f'No Resource Lists to update for tenant: \'{session.tenant}\'', color='yellow')
        print()