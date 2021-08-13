from sdk.load_config import load_config_create_sessions
from sdk.color_print import c_print

from cloud_accounts import cld_migrate
from account_groups import ag_main
from resource_lists import rl_main
from user_roles import role_sync
from user_profiles import users_main
from ip_allow_lists import ip_migrate
from compliance_standards import cmp_migrate
from policies import plc_migrate_custom
from policies import plc_migrate_default
from alert_rules import ar_main
from enterprise_settings import settings_migrate
from anomaly_settings import ano_sync

#PROPER ORDER
#Cloud accounts
#Account Groups
#Resource Lists
#User Roles
#Users
#Trusted IPs
#Compliance Standards
#Saved Searches - done by policy
#Policy
#Alert Rules

def migrate(modes: dict, tenant_sessions: list):
    '''
    Accepts a dictionary of the migrate modes that are enabled and list of tenant session objects.

    Depending on what modes are enabled, call those sync functions.
    '''

    #Checks if element is in the dictionary instead of for a value to keep the data structure
    # similar to the sync modes dictionary.

    #CLOUD ACCOUNT MIGRATE
    if 'cloud' in modes:
        cld_migrate.migrate_cloud_accounts(tenant_sessions)
    #ACCOUNT GROUPS MIGRATE
    if 'account' in modes:
        ag_main.acc_groups(tenant_sessions)
    #RESOURCE LIST MIGRATE
    if 'resource' in modes:
        rl_main.rl_main(tenant_sessions)
    #USER ROLES MIGRATE
    if 'role' in modes:
        role_sync.sync_roles(tenant_sessions, True, False, False)
    #USERS MIGRATE
    if 'user' in modes:
        users_main.users_main(tenant_sessions)
    #TRUSTED IP MIGRATE
    if 'ip' in modes:
        ip_migrate.migrate_trusted_ips(tenant_sessions)
    #COMPLIANCE MIGRATE
    if 'compliance' in modes:
        cmp_migrate.migrate_compliance_standards(tenant_sessions)
    #POLICY MIGRATE
    if 'policy' in modes:
        plc_migrate_custom.migrate_custom_policies(tenant_sessions)
        plc_migrate_default.migrate_builtin_policies(tenant_sessions)
    #ALERT RULES MIGRATE
    if 'alert' in modes:
        ar_main.alert_rules(tenant_sessions)
    if 'anomaly' in modes:
        ano_sync.sync_anomaly_settings(tenant_sessions, True, False, False)
    if 'settings' in modes:
        #Enterprise settings
        settings_migrate.migrate_settings(tenant_sessions)


if __name__ == '__main__':
    migrate()

