from sdk.color_print import c_print

def compare_added_roles(roles_list):
    #Define lists
    original_tenant = roles_list[0]
    clone_tenants = roles_list[1:]

    #Compare the original tenant to the other clone tenants
    clone_tenant_roles_delta = []
    for tenant in clone_tenants:
        roles_delta = []
        for o_role in original_tenant:
            if o_role['name'] not in [role['name'] for role in tenant]:
                roles_delta.append(o_role)

        clone_tenant_roles_delta.append(roles_delta)

    return clone_tenant_roles_delta


def compare_deleted_roles(roles_list):
    #Define lists
    original_tenant = roles_list[0]
    clone_tenants = roles_list[1:]

    #Compare the current tenant to the original tenant
    clone_tenant_roles_delta = []
    for tenant in clone_tenants:
        roles_delta = []
        for role in tenant:
            #If there is a role on the current tenant that does not exist on the 
            # source/original tenant, add it to the list of games that need to be deleted
            if role['name'] not in [o_role['name'] for o_role in original_tenant]:
                roles_delta.append(role)

        clone_tenant_roles_delta.append(roles_delta)

    return clone_tenant_roles_delta

def compare_each_role(roles_list, tenant_sessions=None):
    #Define lists
    original_tenant = roles_list[0]
    clone_tenants = roles_list[1:]

    #Compare the current tenant to the original tenant
    clone_tenant_roles_delta = []
    for index, tenant in enumerate(clone_tenants):
        roles_delta = []
        for role in tenant:
            if role['name'] in [o_role['name'] for o_role in original_tenant]:
                #Get the o_role
                o_role = [o_role for o_role in original_tenant if o_role['name'] == role['name']][0]

                #Add the role to the list if there is a difference
                if compare_roles(o_role, role):
                    #update ID to the role id on the tenant
                    o_role.update(id=role['id'])
                    roles_delta.append(o_role)

        clone_tenant_roles_delta.append(roles_delta)

    return clone_tenant_roles_delta


def compare_roles(role1, role2):
    for r1_item in role1.items():
        #Certain fields are okay to be different
        # if r1_item[0] == 'id' or r1_item[0] == 'lastModifiedBy' or r1_item[0] == 'lastModifiedTs':#FIXME
        if r1_item[0] == 'id' or r1_item[0] == 'lastModifiedBy' or r1_item[0] == 'lastModifiedTs' or r1_item[0] == 'associatedUsers':
            continue
        
        r2_key = r1_item[0]
        r1_val = r1_item[1]

        if r1_val != role2[r2_key]:
            #There is a difference, return
            return True
    #There is no difference, return
    return False

def name_change(role, original_tenant):
    role_desc = role['description']
    role_acc_grp_names = [grp['name'] for grp in role['accountGroups']]
    role_resource_names = [rsc['name'] for rsc in role['resourceLists']]
    role_permission = role['roleType']
    role_dismiss = role['restrictDismissalAccess']
    role_attributes = role['additionalAttributes']

    #If the only attribute that is different is the name, then it is likely the name changed

    for o_role in original_tenant:
        o_role_desc = o_role['description']
        o_role_acc_grp_names = [grp['name'] for grp in o_role['accountGroups']]
        o_role_resource_names = [rsc['name'] for rsc in o_role['resourceLists']]
        o_role_permission = o_role['roleType']
        o_role_dismiss = o_role['restrictDismissalAccess']
        o_role_attributes = role['additionalAttributes']

        if o_role_desc == role_desc and o_role_acc_grp_names == role_acc_grp_names and o_role_resource_names == role_resource_names and o_role_permission == role_permission and o_role_dismiss == role_dismiss and o_role_attributes == role_attributes:
            #Only difference is name, name change event.
            print('Found Name Change Event')
            print()
            return True, o_role['name']
    
    return False