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


    #ADDING AND UPDATING - Order based on dependencies.
    if 'cloud' in modes:
        cld_sync_data = cld_sync.sync(tenant_sessions, modes['cloud'].get('add', True), modes['cloud'].get('up', True), False, logger)
    if 'account' in modes:
        acc_sync_data = acc_sync.sync(tenant_sessions, modes['account'].get('add', True), modes['account'].get('up', True), False)
    if 'resource' in modes:
        rsc_sync_data = rsc_sync.sync(tenant_sessions, modes['resource'].get('add', True), modes['resource'].get('up', True), False)
    if 'role' in modes:
        role_sync_data = role_sync.sync(tenant_sessions, modes['role'].get('add', True), modes['role'].get('up', True), False)
    if 'user' in modes:
        usr_sync_data = usr_sync.sync(tenant_sessions, modes['user'].get('add', True), modes['user'].get('up', True), False)
    if 'ip' in modes:
        ip_sync_data = ip_sync.sync(tenant_sessions, modes['ip'].get('add', True), modes['ip'].get('up', True), False)
    if 'compliance' in modes:
        cmp_sync_data = cmp_sync.sync(tenant_sessions, modes['compliance'].get('add', True), modes['compliance'].get('up', True), False)
    if 'search' in modes:
        search_sync_data = search_sync.sync(tenant_sessions, modes['search'].get('add', True), False)
    if 'policy' in modes:
        plc_sync_data = plc_sync.sync(tenant_sessions, modes['policy'].get('add', True), modes['policy'].get('up', True), False)
    if 'alert' in modes:
        alr_sync_data = alr_sync.sync(tenant_sessions, modes['alert'].get('add', True), modes['alert'].get('up', True), False)
    if 'anomaly' in modes:
        ano_sync_data = ano_sync.sync(tenant_sessions, modes['anomaly'].get('add', True), modes['anomaly'].get('up', True), False)
    if 'settings' in modes:
        set_sync.sync(tenant_sessions)

    #DELETEING - Order based on dependencies
    if 'anomaly' in modes:
        if modes['anomaly'].get('del', False):
            ano_sync.sync(tenant_sessions, False, False, True)

    if 'alert' in modes:
        if modes['alert'].get('del', False):
            alr_sync.sync(tenant_sessions, False, False, True)

    if 'policy' in modes:
        if modes['policy'].get('del', False):
            plc_sync.sync(tenant_sessions, False, False, True)

    if 'search' in modes:
        if modes['search'].get('del', False):
            search_sync.sync(tenant_sessions, False, True)

    if 'compliance' in modes:
        if modes['compliance'].get('del', False):
            cmp_sync.sync(tenant_sessions, False, False, True, cmp_sync_data)

    if 'ip' in modes:
        if modes['ip'].get('del', False):
            ip_sync.sync(tenant_sessions, False, False, True)

    if 'user' in modes:
        if modes['user'].get('del', False):
            usr_sync.sync(tenant_sessions, False, False, True)

    if 'role' in modes:
        if modes['role'].get('del', False):
            role_sync.sync(tenant_sessions, False, False, True)

    if 'resource' in modes:
        if modes['resource'].get('del', False):
            rsc_sync.sync(tenant_sessions, False, False, True)

    if 'cloud' in modes:
        if modes['cloud'].get('del', False):
            cld_sync.sync(tenant_sessions, False, False, True)

    if 'account' in modes:
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
