from tqdm import tqdm

from sdk.load_config import load_config_create_sessions
from sdk.color_print import c_print

from cloud_accounts import cld_sync
from account_groups import acc_sync
from resource_lists import rsc_sync
from user_roles import role_sync
from user_profiles import usr_sync
from ip_allow_lists import ip_sync
from compliance_standards import cmp_sync
from saved_searches import search_sync
from policies import plc_sync
from alert_rules import alr_sync
from anomaly_settings import ano_sync
from enterprise_settings import set_sync

def sync(tenant_sessions: list, modes: dict, logger):
    '''
    Accepts the enabled sync modes dictionary and a list of tenant_session objects.
    
    Depending on what sync modes are enabled, calls the sync functions while 
    specifying the operations that are enabled.
    '''

    run_summary = {}

    mode_list = []
    for mode in modes.items():
        mode_list.append(mode[0])

    #ADDING AND UPDATING - Order based on dependencies.
    for mode in tqdm(mode_list, desc='SYNC ADD/UPDATE STATUS'):
        if 'cloud' == mode:
            added, updated, deleted, cld_sync_data = cld_sync.sync(tenant_sessions, modes['cloud'].get('add', True), modes['cloud'].get('update', True), False, logger)
            run_summary.update(added_cloud_accounts=added)
            run_summary.update(updated_cloud_accounts=updated)
            
        if 'account' == mode:
            added, updated, deleted, acc_sync_data = acc_sync.sync(tenant_sessions, modes['account'].get('add', True), modes['account'].get('update', True), False, logger)
            run_summary.update(added_account_groups=added)
            run_summary.update(updated_account_groups=updated)
        
        if 'resource' == mode:
            added, updated, deleted, rsc_sync_data = rsc_sync.sync(tenant_sessions, modes['resource'].get('add', True), modes['resource'].get('update', True), False, logger)
            run_summary.update(added_resource_lists=added)
            run_summary.update(updated_resource_lists=updated)
        
        if 'role' == mode:
            added, updated, deleted, role_sync_data = role_sync.sync(tenant_sessions, modes['role'].get('add', True), modes['role'].get('update', True), False, logger)
            run_summary.update(added_roles=added)
            run_summary.update(updated_roles=updated)
        
        if 'user' == mode:
            added, updated, deleted, usr_sync_data = usr_sync.sync(tenant_sessions, modes['user'].get('add', True), modes['user'].get('update', True), False, logger)
            run_summary.update(added_profiles=added)
            run_summary.update(updated_profiles=updated)

        if 'ip' == mode:
            added_networks, added_network_cidrs, added_logins, updated_network_cidrs, updated_logins, deleted_network_cidrs, deleted_logins, ip_sync_data = ip_sync.sync(tenant_sessions, modes['ip'].get('add', True), modes['ip'].get('update', True), False, logger)
            run_summary.update(added_networks=added_networks)
            run_summary.update(added_networks_cidrs=added_network_cidrs)
            run_summary.update(added_login_ips=added_logins)
            run_summary.update(updated_network_cidrs=updated_network_cidrs)
            run_summary.update(updated_login_ips=updated_logins)

        if 'compliance' == mode:
            added_standards, added_requirements, added_sections, updated_standards, updated_requirements, updated_sections, deleted_standards, deleted_requirements, deleted_sections, cmp_sync_data = cmp_sync.sync(tenant_sessions, modes['compliance'].get('add', True), modes['compliance'].get('update', True), False, logger)
            run_summary.update(added_standards=added_standards)
            run_summary.update(added_requirements=added_requirements)
            run_summary.update(added_sections=added_sections)
            run_summary.update(updated_standards=updated_standards)
            run_summary.update(updated_requirements=updated_requirements)
            run_summary.update(updated_sections=updated_sections)

        if 'search' == mode:
            added_searches, deleted_searches, search_sync_data = search_sync.sync(tenant_sessions, modes['search'].get('add', True), False, logger)
            run_summary.update(added_searches=added_searches)
        
        if 'policy' == mode:
            added, updated, deleted, updated_default, plc_sync_data = plc_sync.sync(tenant_sessions, modes['policy'].get('add', True), modes['policy'].get('update', True), False, logger)
            run_summary.update(added_policies=added)
            run_summary.update(updated_policies=updated)
            run_summary.update(updated_default_policies=updated_default)
        
        if 'alert' == mode:
            added, updated, deleted, alr_sync_data = alr_sync.sync(tenant_sessions, modes['alert'].get('add', True), modes['alert'].get('update', True), False, logger)
            run_summary.update(added_alerts=added)
            run_summary.update(updated_alerts=updated)
        
        if 'anomaly' == mode:
            added, updated, deleted, ano_sync_data = ano_sync.sync(tenant_sessions, modes['anomaly'].get('add', True), modes['anomaly'].get('update', True), False, logger)
            run_summary.update(added_anomaly=added)
            run_summary.update(updated_anomaly=updated)
            run_summary.update(deleted_anomaly=deleted)
        
        if 'settings' == mode:
            updated = set_sync.sync(tenant_sessions, logger)
            run_summary.update(updated_enterprise_settings=updated)

    #DELETEING - Order based on dependencies
    mode_list = mode_list[::-1]
    #Cloud accounts need to be deleted before account groups
    if 'cloud' in mode_list and 'account' in mode_list:
        mode_list[len(mode_list)-1], mode_list[len(mode_list)-2] = mode_list[len(mode_list)-2], mode_list[len(mode_list)-1]

    for mode in tqdm(mode_list, desc='SYNC DELETE STATUS'):
        if 'anomaly' == mode:
            if modes['anomaly'].get('delete', False):
                added, updated, deleted, ano_sync_data = ano_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_anomaly=deleted)

        if 'alert' == mode:
            if modes['alert'].get('delete', False):
                added, updated, deleted, alr_sync_data = alr_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_alerts=deleted)

        if 'policy' == mode:
            if modes['policy'].get('delete', False):
                added, updated, deleted, updated_default, plc_sync_data = plc_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_policies=deleted)

        if 'search' == mode:
            if modes['search'].get('delete', False):
                added_searches, deleted_searches, search_sync_data = search_sync.sync(tenant_sessions, False, True, logger)
                run_summary.update(deleted_searches=deleted_searches)

        if 'compliance' == mode:
            if modes['compliance'].get('delete', False):
                added_standards, added_requirements, added_sections, updated_standards, updated_requirements, updated_sections, deleted_standards, deleted_requirements, deleted_sections, cmp_sync_data = cmp_sync.sync(tenant_sessions, False, False, True, logger, cmp_sync_data)
                run_summary.update(deleted_standards=deleted_standards)
                run_summary.update(deleted_requirements=deleted_requirements)
                run_summary.update(deleted_sections=deleted_sections)

        if 'ip' == mode:
            if modes['ip'].get('delete', False):
                added_networks, added_network_cidrs, added_logins, updated_network_cidrs, updated_logins, deleted_network_cidrs, deleted_logins, ip_sync_data = ip_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_network_cidrs=deleted_network_cidrs)
                run_summary.update(deleted_logins=deleted_logins)

        if 'user' == mode:
            if modes['user'].get('delete', False):
                added, updated, deleted, usr_sync_data = usr_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_profiles=deleted)

        if 'role' == mode:
            if modes['role'].get('delete', False):
                added, updated, deleted, role_sync_data = role_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_roles=deleted)

        if 'resource' == mode:
            if modes['resource'].get('delete', False):
                added, updated, deleted, rsc_sync_data = rsc_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_resource_lists=deleted)

        if 'cloud' == mode:
            if modes['cloud'].get('delete', False):
                added, updated, deleted, cld_sync_data = cld_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_cloud_accounts=deleted)

        if 'account' == mode:
            if modes['account'].get('delete', False):
                added, updated, deleted, acc_sync_data = acc_sync.sync(tenant_sessions, False, False, True, logger)
                run_summary.update(deleted_cloud_accounts=deleted)

    
    c_print('************************', color='green')
    c_print('Finished syncing tenants', color='green')
    c_print('************************', color='green')
    print()

    print(run_summary)

if __name__ == '__main__':
    sync()


# DELETION ORDER
# Policies - Saved Search - Users - Roles - Resource Lists - Cloud Accounts - Account Groups
# Cant deleteete an account group that is still linked to a cloud account so cloud accounts must be synced/updated first.
