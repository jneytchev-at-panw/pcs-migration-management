# from sdk.load_config import load_config_create_sessions
# from sdk.color_print import c_print

# from cloud_accounts import cld_sync
# from account_groups import ag_sync_main
# from resource_lists import rl_sync_main
# from user_roles import role_sync
# from user_profiles import users_sync_main
# from ip_allow_lists import ip_sync
# from compliance_standards import cmp_sync
# from saved_searches import search_sync
# from policies import plc_sync
# from alert_rules import ar_main
# from anomaly_settings import ano_sync
# from enterprise_settings import settings_migrate

def sync(modes: dict, tenant_sessions: list):
    '''
    Accepts the enabled sync modes dictionary and a list of tenant_session objects.
    
    Depending on what sync modes are enabled, calls the sync functions while 
    specifying the operations that are enabled.
    '''

    if 'cloud' in modes:
        cld_sync.sync_cloud_accounts(tenant_sessions, modes['cloud'].get('add', True), modes['cloud'].get('up', True), modes['cloud'].get('del', True))
    if 'account' in modes:
        ag_sync_main.ag_sync_main(tenant_sessions, modes['account'].get('add', True), modes['account'].get('up', True), modes['account'].get('del', True))
    if 'resource' in modes:
        rl_sync_main.resource_list_sync(tenant_sessions, modes['resource'].get('add', True), modes['resource'].get('up', True), modes['resource'].get('del', True))
    if 'role' in modes:
        role_sync.sync_roles(tenant_sessions, modes['role'].get('add', True), modes['role'].get('up', True), modes['role'].get('del', True))
    if 'user' in modes:
        users_sync_main.users_main(tenant_sessions, modes['user'].get('add', True), modes['user'].get('up', True), modes['user'].get('del', True))
    if 'ip' in modes:
        ip_sync.sync_trusted_ips(tenant_sessions, modes['ip'].get('add', True), modes['ip'].get('up', True), modes['ip'].get('del', True))
    if 'compliance' in modes:
        cmp_sync.sync_compliance(tenant_sessions, modes['compliance'].get('add', True), modes['compliance'].get('up', True), modes['compliance'].get('del', True))
    if 'search' in modes:
        search_sync.sync_search(tenant_sessions, modes['search'].get('add', True), modes['search'].get('del', True))
    if 'policy' in modes:
        plc_sync.sync_policies(tenant_sessions, modes['policy'].get('add', True), modes['policy'].get('up', True), modes['policy'].get('del', True))
    if 'alert' in modes:
        ar_main.alert_rules(tenant_sessions, modes['alert'].get('add', True), modes['alert'].get('up', True), modes['alert'].get('del', True))
    if 'anomaly' in modes:
        ano_sync.sync_anomaly_settings(tenant_sessions, modes['anomaly'].get('add', True), modes['anomaly'].get('up', True), modes['anomaly'].get('del', True))
    if 'settings' in modes:
        settings_migrate.migrate_settings(tenant_sessions)

if __name__ == '__main__':
    sync()


# DELETION ORDER
# Users - Roles - Resource Lists - Cloud Accounts - Account Groups