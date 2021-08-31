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

    mode_list = []
    for mode in modes.items():
        mode_list.append(mode[0])

    #ADDING AND UPDATING - Order based on dependencies.
    for mode in tqdm(mode_list, desc='Sync Add Update Status'):
        if 'cloud' == mode:
            cld_sync_data = cld_sync.sync(tenant_sessions, modes['cloud'].get('add', True), modes['cloud'].get('up', True), False, logger)
        if 'account' == mode:
            acc_sync_data = acc_sync.sync(tenant_sessions, modes['account'].get('add', True), modes['account'].get('up', True), False, logger)
        if 'resource' == mode:
            rsc_sync_data = rsc_sync.sync(tenant_sessions, modes['resource'].get('add', True), modes['resource'].get('up', True), False)
        if 'role' == mode:
            role_sync_data = role_sync.sync(tenant_sessions, modes['role'].get('add', True), modes['role'].get('up', True), False)
        if 'user' == mode:
            usr_sync_data = usr_sync.sync(tenant_sessions, modes['user'].get('add', True), modes['user'].get('up', True), False)
        if 'ip' == mode:
            ip_sync_data = ip_sync.sync(tenant_sessions, modes['ip'].get('add', True), modes['ip'].get('up', True), False)
        if 'compliance' == mode:
            cmp_sync_data = cmp_sync.sync(tenant_sessions, modes['compliance'].get('add', True), modes['compliance'].get('up', True), False)
        if 'search' == mode:
            search_sync_data = search_sync.sync(tenant_sessions, modes['search'].get('add', True), False)
        if 'policy' == mode:
            plc_sync_data = plc_sync.sync(tenant_sessions, modes['policy'].get('add', True), modes['policy'].get('up', True), False)
        if 'alert' == mode:
            alr_sync_data = alr_sync.sync(tenant_sessions, modes['alert'].get('add', True), modes['alert'].get('up', True), False)
        if 'anomaly' == mode:
            ano_sync_data = ano_sync.sync(tenant_sessions, modes['anomaly'].get('add', True), modes['anomaly'].get('up', True), False)
        if 'settings' == mode:
            set_sync.sync(tenant_sessions)

    #DELETEING - Order based on dependencies
    for mode in tqdm(mode_list, desc='Sync Delete Status'):
        if 'anomaly' == mode:
            if modes['anomaly'].get('del', False):
                ano_sync.sync(tenant_sessions, False, False, True)

        if 'alert' == mode:
            if modes['alert'].get('del', False):
                alr_sync.sync(tenant_sessions, False, False, True)

        if 'policy' == mode:
            if modes['policy'].get('del', False):
                plc_sync.sync(tenant_sessions, False, False, True)

        if 'search' == mode:
            if modes['search'].get('del', False):
                search_sync.sync(tenant_sessions, False, True)

        if 'compliance' == mode:
            if modes['compliance'].get('del', False):
                cmp_sync.sync(tenant_sessions, False, False, True, cmp_sync_data)

        if 'ip' == mode:
            if modes['ip'].get('del', False):
                ip_sync.sync(tenant_sessions, False, False, True)

        if 'user' == mode:
            if modes['user'].get('del', False):
                usr_sync.sync(tenant_sessions, False, False, True)

        if 'role' == mode:
            if modes['role'].get('del', False):
                role_sync.sync(tenant_sessions, False, False, True)

        if 'resource' == mode:
            if modes['resource'].get('del', False):
                rsc_sync.sync(tenant_sessions, False, False, True)

        if 'cloud' == mode:
            if modes['cloud'].get('del', False):
                cld_sync.sync(tenant_sessions, False, False, True)

        if 'account' == mode:
            if modes['account'].get('del', False):
                acc_sync.sync(tenant_sessions, False, False, True, logger)
    
    c_print('************************', color='green')
    c_print('Finished syncing tenants', color='green')
    c_print('************************', color='green')
    print()

if __name__ == '__main__':
    sync()


# DELETION ORDER
# Policies - Saved Search - Users - Roles - Resource Lists - Cloud Accounts - Account Groups
# Cant delete an account group that is still linked to a cloud account so cloud accounts must be synced/updated first.
