from sdk.color_print import c_print

def compare_trusted_networks(source_networks, clone_networks):
    '''
    Accepts the source trusted alert network list and a clone trusted alert network list.

    Compares the source tenants network list to a clone tenant networks list.
    '''

    networks_delta = []
    for src_network in source_networks:
        if src_network['name'] not in [network['name'] for network in clone_networks]:
            networks_delta.append(src_network)

    return networks_delta

#Sync
# def compare_each_network_cidr_and_add(tenant_sessions, source_networks, clone_networks):

#     #Define lists
#     for src_network in source_networks:
#         #Check if all cidr blocks are present
#         new_network = [network for network in tenant if network['name'] == o_network['name']][0]
#         if not new_network:
#             #network would have just been added, can't update it here
#             break
#         cidr_to_add = []
#         for cidr in o_network['cidrs']:
#             if cidr['cidr'] not in [n_cidr['cidr'] for n_cidr in new_network['cidrs']]:
#                 cidr_to_add.append(cidr)
#         net_name = o_network['name']
#         for cidr in cidr_to_add:
#             networkUuid = new_network['uuid']
#             c_print(f'API - Adding cidrs to network {net_name}')
#             tenant_sessions[index + 1].request('POST', f'/allow_list/network/{networkUuid}/cidr', json=cidr)

#Sync
# def compare_each_network_cidr_and_update(tenant_sessions, network_list):
#     #Define lists
#     original_tenant = network_list[0]
#     clone_tenants = network_list[1:]
#     for index, tenant in enumerate(clone_tenants):
#         for o_network in original_tenant:
#             for c_network in tenant:
#                 #Check if all cidr blocks are present
#                 cidrs_to_update = []
#                 for o_cidr in o_network['cidrs']:
#                     for c_cidr in c_network['cidrs']:
#                         if o_cidr['cidr'] == c_cidr['cidr'] and o_cidr.get('description', '') != c_cidr.get('description', ''):
#                             c_cidr.update(description=o_cidr['description'])
#                             cidrs_to_update.append(c_cidr)

#                 for cidr in cidrs_to_update:
#                     networkUuid = c_network['uuid']
#                     name = c_network['name']
#                     c_id = cidr['uuid']
#                     c_print(f'API - Updating cidr on network {name}')
#                     tenant_sessions[index + 1].request('PUT', f'/allow_list/network/{networkUuid}/cidr/{c_id}', json=cidr)

#Sync
# def compare_each_network_cidr_and_delete(tenant_sessions, network_list):
#     #Define lists
#     original_tenant = network_list[0]
#     source_session = tenant_sessions[0]
#     clone_tenants = network_list[1:]
#     clone_sessions = tenant_sessions[1:]

#     clone_tenant_networks_delta = []
#     for tenant, session in zip(clone_tenants, clone_sessions):
#         networks_delta = []
#         for o_network in original_tenant:
#             for c_network in tenant:
#                 if o_network['name'] == c_network['name']:
#                     name = o_network['name']
#                     networkUuid = c_network['uuid']
                
#                     #Get cidr that needs to be deleted
#                     cidrs_to_delete = []
#                     for c_cidr in c_network['cidrs']:
#                         if c_cidr['cidr'] not in [ci['cidr'] for ci in o_network['cidrs']]:
#                             cidrs_to_delete.append(c_cidr) #We need the cidr and the uuid for deletion
#                     #Delete the cidrs from the destination tenant
#                     for cidr in cidrs_to_delete:
#                         cidrUuid = cidr['uuid']
#                         c_print(f'API - Deleting cidr from network: \'{name}\'')
#                         session.request('DELETE', f'/allow_list/network/{networkUuid}/cidr/{cidrUuid}')

#Sync
# def compare_cidr_lists(src_cidrs: list, cln_cidrs: list):
#     cidrs_to_add = []
#     for cidr in src_cidrs['cidr']:
#         if cidr not in cln_cidrs['cidr']:
#             cidrs_to_add.append(cidr)

#     return cidrs_to_add

def compare_login_ips(src_logins, cln_logins):
    '''
    Accepts the list of src trusted logins and a list of clone trusted logins.

    Returns the lists of trusted logins found in the source that are not found in the clone.
    '''
    ips_delta = []
    for src_network in src_logins:
        if src_network['name'] not in [network['name'] for network in cln_logins]:
            ips_delta.append(src_network)

    return ips_delta

#Sync
# def compare_each_login_ip(login_lists):
#     #Define lists
#     original_tenant = login_lists[0]
#     clone_tenants = login_lists[1:]

#     #Compare the original tenant to the other clone tenants
#     clone_tenant_ips_delta = []
#     for tenant in clone_tenants:
#         ips_delta = []
#         for o_network in original_tenant:
#             for c_network in tenant:
#                 if o_network['cidr'] != c_network['cidr'] or o_network['description'] != c_network['description']:
#                     ips_delta.append(o_network)

#         clone_tenant_ips_delta.append(ips_delta)

#     return clone_tenant_ips_delta

#Sync
# def compare_login_ip_to_delete(login_lists):
#     #Define lists
#     original_tenant = login_lists[0]
#     clone_tenants = login_lists[1:]

#     #Compare the original tenant to the other clone tenants
#     clone_tenant_ips_delta = []
#     for tenant in clone_tenants:
#         ips_delta = []
#         for d_network in tenant:
#             if d_network['name'] not in [o_network['name'] for o_network in original_tenant]:
#                 ips_delta.append(d_network)
        
#         clone_tenant_ips_delta.append(ips_delta)

#     return clone_tenant_ips_delta