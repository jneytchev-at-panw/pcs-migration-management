from sdk.color_print import c_print

def delete_roles(session, roles):
    if roles:
        c_print(f'Deleting User Roles from tenant: \'{session.tenant}\'', color='blue')
        print()

        for role in roles:
            r_id = role['id']
            name = role['name']
            c_print(f'API - Deleting role {name}')
            session.request('DELETE', f'/user/role/{r_id}', json=role)

    else:
        c_print(f'No User Roles to delete for tenant: \'{session.tenant}\'', color='yellow')
        print()