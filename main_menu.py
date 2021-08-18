from main_scripts import migrate_main, sync_main
from sdk.color_print import c_print
from sdk.load_config import load_config_create_sessions

def build_module():
    module_dict = {}
    full = input('Do you want to enable Add, Update, and Delete operations? (Y/N): ')
    full = full.lower()
    if full =='y' or full =='yes':
        module_dict.update(add=True)
        module_dict.update(up=True)
        module_dict.update(delete=True)
        return module_dict
    else:
        add = input('Do you want to enable the Add operation? (Y/N): ')
        add = add.lower()
        if add == 'y' or add == 'yes':
            module_dict.update(add=True)
        else:
            module_dict.update(add=False)

        up = input('Do you want to enable the Update operation? (Y/N): ')
        up = up.lower()
        if up == 'y' or up =='yes':
            module_dict.update(update=True)
        else:
            module_dict.update(update=False)

        del_ = input('Do you want to enable the Delete operation? (Y/N): ')
        del_ = del_.lower()
        if del_ == 'y' or del_ =='yes':
            module_dict.update(delete=True)
        else:
            module_dict.update(delete=False)

        return module_dict

def load_config():
    '''
    Returns the tenant sessions, config settings, and a flag for same-stack syncing/migration detected.
    '''

    tenant_sessions = load_config_create_sessions()

    settings = {}

    same_stack = False
    for session in tenant_sessions:
        current = session.api_url
        found = 0

        for session2 in tenant_sessions:
            if current == session2.api_url:
                found += 1

        if found > 1:
            same_stack = True

    return(tenant_sessions, settings, same_stack)



if __name__ == '__main__':

    tenant_sessions, settings, same_stack = load_config()

    mode = input('Do you want to Migrate or Sync? (M/S): ')
    print()

    mode = mode.lower() 
    if mode == 'm' or mode == 'migrate':#--------------------------------------------------
        migrate_type = input('Do you want to do a full Migration? (Y/N): ')
        print()
        migrate_type = migrate_type.lower()

        migrate_modes = {
            'cloud': {},
            'account': {},
            'resource': {},
            'role': {},
            'user': {},
            'ip': {},
            'compliance': {},
            'policy': {},
            'alert': {},
            'anomaly': {},
            'settings': {}
        }
        
        if migrate_type == 'y' or migrate_type == 'yes':
            migrate_main.migrate(tenant_sessions, migrate_modes)
        else:
            enabled = input('Do you want to migrate Cloud Accounts? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('cloud')
            print()

            enabled = input('Do you want to migrate Account Groups? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('account')
            print()

            enabled = input('Do you want to migrate Resource Lists? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('resource')
            print()

            enabled = input('Do you want to migrate Roles? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('role')
            print()

            enabled = input('Do you want to migrate Users? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('user')
            print()

            enabled = input('Do you want to migrate Trusted IPs? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('ip')
            print()

            enabled = input('Do you want to migrate Compliance Data? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('compliance')
            print()

            enabled = input('Do you want to migrate Policies? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('policy')
            print()

            enabled = input('Do you want to migrate Alert Rules? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('alert')
            print()

            enabled = input('Do you want to migrate Anomaly Settings? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('anomaly')
            print()

            enabled = input('Do you want to migrate Enterprise Settings? (Y/N): ')
            enabled = enabled.lower()
            if enabled != 'y' or enabled != 'yes':
                migrate_modes.pop('settings')
            print()
            
            #Call migrate module
            migrate_main.migrate(migrate_modes)

    else:#---------------------------------------------------------------------------------
        migrate_type = input('Do you want to do a full Sync? (Y/N): ')
        print()
        migrate_type = migrate_type.lower()

        sync_modes = {
            'cloud': {},
            'account': {},
            'resource': {},
            'role': {},
            'user': {},
            'ip': {},
            'compliance': {},
            'search': {},
            'policy': {},
            'alert': {},
            'anomaly': {},
            'settings': {}
        }

        if migrate_type == 'y' or migrate_type == 'yes':
            sync_main.sync(sync_modes)
        else:
            enabled = input('Do you want to sync Cloud Accounts? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(cloud=mode_dict)
            else:
                sync_modes.pop('cloud')
            print()

            enabled = input('Do you want to sync Account Groups? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(account=mode_dict)
            else:
                sync_modes.pop('account')
            print()

            enabled = input('Do you want to sync Resource Lists? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(resource=mode_dict)
            else:
                sync_modes.pop('resource')
            print()

            enabled = input('Do you want to sync Roles? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(role=mode_dict)
            else:
                sync_modes.pop('role')
            print()

            enabled = input('Do you want to sync Users? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(user=mode_dict)
            else:
                sync_modes.pop('user')
            print()

            enabled = input('Do you want to sync Trusted IPs? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(ip=mode_dict)
            else:
                sync_modes.pop('ip')
            print()

            enabled = input('Do you want to sync Compliance Data? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(compliance=mode_dict)
            else:
                sync_modes.pop('compliance')
            print()

            enabled = input('Do you want to sync Saved Searches? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(search=mode_dict)
            else:
                sync_modes.pop('search')
            print()

            enabled = input('Do you want to sync Policies? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(policy=mode_dict)
            else:
                sync_modes.pop('policy')
            print()

            enabled = input('Do you want to sync Alert Rules? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(alert=mode_dict)
            else:
                sync_modes.pop('alert')
            print()

            enabled = input('Do you want to sync Anomaly Settings? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled == 'yes':
                mode_dict = build_module()
                sync_modes.update(anomaly=mode_dict)
            else:
                sync_modes.pop('anomaly')
            print()
            
            #Call sync module
            sync_main.sync(sync_modes)


        
        

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


