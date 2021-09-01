from sdk.color_print import c_print
from tqdm import tqdm

def add_networks(session, networks, logger):
    '''
    Accepts a tenant session object and a list of networks.

    Adds each network and then dispatches function to add the network cidrs
    '''

    if networks:
        logger.info(f'Adding Trusted Alert IP Networks to tenant: \'{session.tenant}\'')

        for network in tqdm(networks, desc='Adding Networks', leave=False):
            logger.debug('API - Adding Trusted Alert IP Network')
            res = session.request('POST', '/allow_list/network', json=network)
            data = res.json()
            add_network_cidrs(session, data, network['cidr'])
    else:
        logger.info(f'No Trusted Alert IP Networks to add for tenant: \'{session.tenant}\'')

#==============================================================================

def add_network_cidrs(session, network, cidrs, logger):
    '''
    Accepts a tenant session, network and a cidr lists.

    Adds network ciders to each given network.
    '''
    if cidrs:
        logger.info(f'Adding Network CIDRs to tenant: \'{session.tenant}\'')

        networkUuid = network['uuid']
        name = network['name']
        for cidr in tqdm(cidrs, desc='Adding Network CIDRs', leave=False):
            #upload each cider in a network
            logger.debug(f'API - Adding cidr blocks to network{name}')
            session.request('POST', f'/network/{networkUuid}/cidr', json=cidr, redlock_ignore=['duplicate_public_network'])
    else:
        logger.info(f'No Network Cidrs to add for tenant: \'{session.tenant}\'')


#==============================================================================

def add_network_allow_list_cidrs(session, net_uuid, cidrs, logger):
    '''
    Accepts a tenant session, the network uuid, and a list of cidrs.

    Adds all cidr blocks to the network with the provided UUID.
    '''

    if cidrs:
        for cidr in tqdm(cidrs, desc='Adding CIDRs to network', leave=False):
            logger.debug('API - Adding CIDRs to network')
            session.request('POST', f'/allow_list/network/{net_uuid}/cidr', json=cidr)



def add_login_ips(session, ips, logger):
    '''
    Accepts a tenant session and a list of Login Allow IPs.

    Adds the Login Allow IPs.
    '''
    if ips:
        logger.info(f'Adding Login IPs to tenant: \'{session.tenant}\'')

        for ip in ips:
            logger.debug('API - Adding login allow IP')
            session.request('POST', '/ip_allow_list_login', json=ip)
    else:
        logger.info(f'No Login IPs to add for tenant: \'{session.tenant}\'')