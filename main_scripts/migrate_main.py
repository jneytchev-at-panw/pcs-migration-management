from sdk.load_config import load_config_create_sessions
from sdk.color_print import c_print

from cloud_accounts import cld_migrate
from account_groups import acc_migrate
from resource_lists import rsc_migrate
from user_roles import role_migrate
from user_profiles import usr_migrate
from ip_allow_lists import ip_migrate
from compliance_standards import cmp_migrate
from policies import plc_migrate_custom
from policies import plc_migrate_default
from alert_rules import alr_migrate
from enterprise_settings import set_sync
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

def migrate(tenant_sessions: list, modes: dict):
    '''
    Accepts a dictionary of the migrate modes that are enabled and list of tenant session objects.

    Depending on what modes are enabled, call those sync functions.
    '''

    #Checks if element is in the dictionary instead of for a value to keep the data structure
    # similar to the sync modes dictionary.

    #CLOUD ACCOUNT MIGRATE
    if 'cloud' in modes:
        cld_migrate.migrate(tenant_sessions)
    #ACCOUNT GROUPS MIGRATE
    if 'account' in modes:
        acc_migrate.migrate(tenant_sessions)
    #RESOURCE LIST MIGRATE
    if 'resource' in modes:
        rsc_migrate.migrate(tenant_sessions)
    #USER ROLES MIGRATE
    if 'role' in modes:
        role_migrate.migrate(tenant_sessions)
    #USERS MIGRATE
    if 'user' in modes:
        usr_migrate.migrate(tenant_sessions)
    #TRUSTED IP MIGRATE
    if 'ip' in modes:
        ip_migrate.migrate(tenant_sessions)
    #COMPLIANCE MIGRATE
    if 'compliance' in modes:
        cmp_migrate.migrate(tenant_sessions)
    #POLICY MIGRATE
    if 'policy' in modes:
        plc_migrate_custom.migrate_custom_policies(tenant_sessions)
        plc_migrate_default.migrate_builtin_policies(tenant_sessions)
    #ALERT RULES MIGRATE
    if 'alert' in modes:
        alr_migrate.migrate(tenant_sessions)
    if 'anomaly' in modes:
        ano_sync.sync(tenant_sessions, True, False, False)
    if 'settings' in modes:
        #Enterprise settings
        set_sync.sync(tenant_sessions)

    c_print('**************************', color='green')
    c_print('Finished migrating tenants', color='green')
    c_print('**************************', color='green')
    print()


if __name__ == '__main__':
    migrate()

