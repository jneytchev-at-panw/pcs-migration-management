from sdk.color_print import c_print

#Migrate
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
def compare_each_network_cidr_and_add(session, source_networks, clone_networks):
    #Define lists
    for src_network in source_networks:
        #Check if all cidr blocks are present
        new_network = [network for network in clone_networks if network['name'] == src_network['name']][0]
        if not new_network:
            #network would have just been added, can't update it here
            break
        cidr_to_add = []
        for cidr in src_network['cidrs']:
            if cidr['cidr'] not in [n_cidr['cidr'] for n_cidr in new_network['cidrs']]:
                cidr_to_add.append(cidr)
        net_name = src_network['name']
        for cidr in cidr_to_add:
            networkUuid = new_network['uuid']
            c_print(f'API - Adding cidrs to network {net_name}')
            session.request('POST', f'/allow_list/network/{networkUuid}/cidr', json=cidr)

#Sync
def compare_each_network_cidr_and_update(session, source_networks, clone_networks):
    for src_network in source_networks:
        for cln_network in clone_networks:
            #Check if all cidr blocks are present
            cidrs_to_update = []
            for s_cidr in src_network['cidrs']:
                for c_cidr in cln_network['cidrs']:
                    if s_cidr['cidr'] == c_cidr['cidr'] and s_cidr.get('description', '') != c_cidr.get('description', ''):
                        c_cidr.update(description=s_cidr['description'])
                        cidrs_to_update.append(c_cidr)

            for cidr in cidrs_to_update:
                networkUuid = cln_network['uuid']
                name = cln_network['name']
                c_id = cidr['uuid']
                c_print(f'API - Updating cidr on network {name}')
                session.request('PUT', f'/allow_list/network/{networkUuid}/cidr/{c_id}', json=cidr)

#Sync
def compare_each_network_cidr_and_delete(session, source_networks, clone_networks):
    networks_delta = []
    for src_network in source_networks:
        for cln_network in clone_networks:
            if src_network['name'] ==cln_network['name']:
                name = src_network['name']
                networkUuid =cln_network['uuid']
            
                #Get cidr that needs to be deleted
                cidrs_to_delete = []
                for c_cidr in cln_network['cidrs']:
                    if c_cidr['cidr'] not in [ci['cidr'] for ci in src_network['cidrs']]:
                        cidrs_to_delete.append(c_cidr) #We need the cidr and the uuid for deletion
                #Delete the cidrs from the destination tenant
                for cidr in cidrs_to_delete:
                    cidrUuid = cidr['uuid']
                    c_print(f'API - Deleting cidr from network: \'{name}\'')
                    session.request('DELETE', f'/allow_list/network/{networkUuid}/cidr/{cidrUuid}')

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
def compare_each_login_ip(src_login_ips, cln_login_ips):
    ips_delta = []
    for src_network in src_login_ips:
        for cln_network in cln_login_ips:
            if src_network['cidr'] != cln_network['cidr'] or src_network['description'] != cln_network['description']:
                ips_delta.append(src_network)

    return ips_delta

#Sync
def compare_login_ip_to_delete(src_login_ips, cln_login_ips):
    ips_delta = []
    for cln_network in cln_login_ips:
        if cln_network['name'] not in [o_network['name'] for o_network in src_login_ips]:
            ips_delta.append(cln_network)

    return ips_delta