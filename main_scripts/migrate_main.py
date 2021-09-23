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

    run_summary = {}

    for mode in tqdm(mode_list, desc='MIGRATION STATUS'):
        #CLOUD ACCOUNT MIGRATE
        if 'cloud' == mode:
            added = cld_migrate.migrate(tenant_sessions, logger)
        run_summary.update(added_cloud_accounts=added)

        #ACCOUNT GROUPS MIGRATE
        if 'account' == mode:
            added = acc_migrate.migrate(tenant_sessions, logger)
        run_summary.update(added_account_groups=added)

        #RESOURCE LIST MIGRATE
        if 'resource' == mode:
            added = rsc_migrate.migrate(tenant_sessions, logger)
        run_summary.update(added_resource_lists=added)

        #USER ROLES MIGRATE
        if 'role' == mode:
            added = role_migrate.migrate(tenant_sessions, logger)
        run_summary.update(added_user_roles=added)

        #USERS MIGRATE
        if 'user' == mode:
            added = usr_migrate.migrate(tenant_sessions, logger)
        run_summary.update(added_user_profiles=added)
        
        #TRUSTED IP MIGRATE
        if 'ip' == mode:
            tenant_networks_added, tenant_cidrs_added, tenant_login_ips_added = ip_migrate.migrate(tenant_sessions, logger)
        run_summary.update(added_networks=tenant_networks_added)
        run_summary.update(added_cidrs=tenant_cidrs_added)
        run_summary.update(added_login_ips=tenant_login_ips_added) 

        #COMPLIANCE MIGRATE
        if 'compliance' == mode:
            standards_added, requirements_added, sections_added = cmp_migrate.migrate(tenant_sessions, logger)
        run_summary.update(added_compliance_standards=standards_added)
        run_summary.update(added_compliance_requirements=requirements_added)
        run_summary.update(added_compliance_sections=sections_added)

        
        #POLICY MIGRATE
        if 'policy' == mode:
            added = plc_migrate_custom.migrate_custom_policies(tenant_sessions, logger)
            run_summary.update(added_custom_policies=added)

            added = plc_migrate_default.migrate_builtin_policies(tenant_sessions, logger)
            run_summary.update(updated_default_policies=added)
        
        #ALERT RULES MIGRATE
        if 'alert' == mode:
            added = alr_migrate.migrate(tenant_sessions, logger)
            run_summary.update(added_alert_rules)
            
        
        if 'anomaly' == mode:
            added_trusted_lists = ano_sync.sync(tenant_sessions, True, False, False, logger)
            run_summary.update(added_trusted_lists=added_trusted_lists)


        if 'settings' == mode:
            #Enterprise settings
            updated = set_sync.sync(tenant_sessions, logger)
            run_summary.update(updated_enterprise_settings=updated)

    c_print('**************************', color='green')
    c_print('Finished migrating tenants', color='green')
    c_print('**************************', color='green')
    print()


if __name__ == '__main__':
    migrate()

