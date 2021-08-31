from tqdm import tqdm

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

def migrate(tenant_sessions: list, modes: dict, logger: object):
    '''
    Accepts a dictionary of the migrate modes that are enabled and list of tenant session objects.

    Depending on what modes are enabled, call those sync functions.
    '''

    #Checks if element is in the dictionary instead of for a value to keep the data structure
    # similar to the sync modes dictionary.

    mode_list = []
    for mode in modes.items():
        mode_list.append(mode[0])

    for mode in tqdm(mode_list, desc='Migration Status'):
        #CLOUD ACCOUNT MIGRATE
        if 'cloud' == mode:
            cld_migrate.migrate(tenant_sessions, logger)
        #ACCOUNT GROUPS MIGRATE
        if 'account' == mode:
            acc_migrate.migrate(tenant_sessions, logger)
        #RESOURCE LIST MIGRATE
        if 'resource' == mode:
            rsc_migrate.migrate(tenant_sessions, logger)
        #USER ROLES MIGRATE
        if 'role' == mode:
            role_migrate.migrate(tenant_sessions, logger)
        #USERS MIGRATE
        if 'user' == mode:
            usr_migrate.migrate(tenant_sessions, logger)
        #TRUSTED IP MIGRATE
        if 'ip' == mode:
            ip_migrate.migrate(tenant_sessions, logger)
        #COMPLIANCE MIGRATE
        if 'compliance' == mode:
            cmp_migrate.migrate(tenant_sessions, logger)
        #POLICY MIGRATE
        if 'policy' == mode:
            plc_migrate_custom.migrate_custom_policies(tenant_sessions, logger)
            plc_migrate_default.migrate_builtin_policies(tenant_sessions, logger)
        #ALERT RULES MIGRATE
        if 'alert' == mode:
            alr_migrate.migrate(tenant_sessions, logger)
        if 'anomaly' == mode:
            ano_sync.sync(tenant_sessions, True, False, False, logger)
        if 'settings' == mode:
            #Enterprise settings
            set_sync.sync(tenant_sessions, logger)

    c_print('**************************', color='green')
    c_print('Finished migrating tenants', color='green')
    c_print('**************************', color='green')
    print()


if __name__ == '__main__':
    migrate()

