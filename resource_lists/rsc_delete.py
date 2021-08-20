from sdk.color_print import c_print

def delete_resource_lists(session, resource_lists):
    if resource_lists:
        c_print(f'Deleteing resource lists from tenant: \'{session.tenant}\'', color='green')
        print()

        for rsc_list in resource_lists:
            rl_id = rsc_list['id']
            status_ignore = [201, 204]
            print('API - Deleting Resource List')
            session.request("DELETE", f"/v1/resource_list/{rl_id}", status_ignore=status_ignore)

    else:
        c_print(f'No Resource Lists to delete for tenant: \'{session.tenant}\'', color='yellow')
        print()