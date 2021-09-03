from ip_allow_lists import ip_add, ip_compare, ip_get, ip_update, ip_delete
from sdk.color_print import c_print

def sync(tenant_sessions: list, addMode: bool, upMode: bool, delMode: bool, logger):
    #Get trusted ips from the tenants
    trusted_networks_list = []
    for session in tenant_sessions:
        networks = ip_get.get_trusted_networks(session, logger)
        trusted_networks_list.append(networks)

    #Define network lists
    src_network = trusted_networks_list[0]
    clone_networks = trusted_networks_list[1:]
    clone_tenant_sessions = tenant_sessions[1:]

    if addMode:
        #Get the trusted network networks that are needed to be added=========================================
        trusted_networks_delta = []
        for cln_network in clone_networks:
            ips = ip_compare.compare_trusted_networks(src_network, cln_network)
            trusted_networks_delta.append(ips)

        #Upload networks to clone tenants
        for index, networks in enumerate(trusted_networks_delta):
            tenant_session = clone_tenant_sessions[index]
            ip_add.add_networks(tenant_session, networks, logger)

    #Get trusted networks that need to be updated=========================================================
    if addMode:
        #Add cidr blocks to networks as needed
        for index, cln_network in enumerate(clone_networks):
            ip_compare.compare_each_network_cidr_and_add(tenant_sessions[index + 1], src_network, cln_network, logger)
    if delMode:
        #Delete cidr blocks from networks as needed
        for index, cln_network in enumerate(clone_networks):
            ip_compare.compare_each_network_cidr_and_delete(tenant_sessions[index + 1], src_network, cln_network, logger)
    if upMode:
        #Update description of network ips
        for index, cln_network in enumerate(clone_networks):
            ip_compare.compare_each_network_cidr_and_update(tenant_sessions[index + 1], src_network, cln_network, logger)
    

    #Trusted Login IP Sync===============================================================================
    #Get login ips
    login_ips_list = []
    for session in tenant_sessions:
        ips = ip_get.get_login_ips(session, logger)
        login_ips_list.append(ips)

    src_login_ips = login_ips_list[0]
    clone_login_ips = login_ips_list[1:]

    if addMode:
        login_ips_delta = []
        #Get the login ips that need to be added
        for cln_login_ips in clone_login_ips:
            ips = ip_compare.compare_login_ips(src_login_ips, cln_login_ips)
            login_ips_delta.append((ips))

        #Upload login IPs to clone tenants
        for index, ips in enumerate(login_ips_delta):
            tenant_session = clone_tenant_sessions[index]
            ip_add.add_login_ips(tenant_session, ips, logger)

    if upMode:
        login_ips_delta = []
        #Get the login IPs that need to be updated
        for cln_login_ips in clone_login_ips:
            ips = ip_compare.compare_each_login_ip(src_login_ips, cln_login_ips)
            login_ips_delta.append(ips)

        for index, ips in enumerate(login_ips_delta):
            tenant_session = clone_tenant_sessions[index]
            ip_update.update_login_ips(tenant_session, ips, login_ips_list[index + 1], logger)

    if delMode:
        login_ips_delta = []
        #Get the login IPs that need to be updated
        for cln_login_ips in clone_login_ips:
            ips = ip_compare.compare_login_ip_to_delete(src_login_ips, cln_login_ips)
            login_ips_delta.append(ips)

        for index, ips in enumerate(login_ips_delta):
            tenant_session = clone_tenant_sessions[index]
            ip_delete.delete_login_ips(tenant_session, ips,  login_ips_list[index + 1], logger)

    logger.info('Finished syncing IP Allow Lists')

if __name__ == '__main__':
    from sdk.load_config import load_config_create_sessions
    tenant_sessions = load_config_create_sessions()

    sync(tenant_sessions, True, True, True)