from sdk.color_print import c_print

def add_networks(session, networks):
    '''
    Accepts a tenant session object and a list of networks.

    Adds each network and then dispatches function to add the network cidrs
    '''

    if networks:
        c_print('Adding Trusted Alert IP Networks', color='blue')
        print()

        for network in networks:
            c_print('API - Adding Trusted Alert IP Network')
            res = session.request('POST', '/allow_list/network', json=network)
            data = res.json()
            add_network_cidrs(session, data, network['cidr'])
    else:
        c_print('No Trusted Alert IP Networks to add', color='yellow')
        print()

def add_network_cidrs(session, network, cidrs):
    '''
    Accepts a tenant session, network and a cidr lists.

    Adds network ciders to each given network.
    '''
    networkUuid = network['uuid']
    name = network['name']
    for cidr in cidrs:
        #upload each cider in a network
        c_print(f'API - Adding cidr blocks to network{name}')
        session.request('POST', f'/network/{networkUuid}/cidr', json=cidr, redlock_ignore=['duplicate_public_network'])

def add_network_allow_list_cidrs(session, net_uuid, cidrs):
    '''
    Accepts a tenant session, the network uuid, and a list of cidrs.

    Adds all cidr blocks to the network with the provided UUID.
    '''
    
    for cidr in cidrs:
        print('API Adding CIDRs to network')
        session.request('POST', f'/allow_list/network/{net_uuid}/cidr', json=cidr)


def add_login_ips(session, ips):
    '''
    Accepts a tenant session and a list of Login Allow IPs.

    Adds the Login Allow IPs.
    '''
    if ips:
        c_print('Adding Login IPs', color='blue')
        print()

        for ip in ips:
            c_print('API - Adding login allow IP',)
            session.request('POST', '/ip_allow_list_login', json=ip)
    else:
        c_print('No Login IPs to add', color='yellow')
        print()