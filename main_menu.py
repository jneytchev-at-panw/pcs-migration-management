import json
from main_scripts import migrate_main, sync_main
from sdk.color_print import c_print
from sdk.load_config import load_config_create_sessions

#Build the dictionary used for sync to determin if the module should support the update, add and delete operations
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

#Read credentials config file
def load_sessions():
    '''
    Returns the tenant sessions, config settings, and a flag for same-stack syncing/migration detected.
    '''

    tenant_sessions = load_config_create_sessions()

    same_stack = False
    for session in tenant_sessions:
        current = session.api_url
        found = 0

        for session2 in tenant_sessions:
            if current == session2.api_url:
                found += 1

        if found > 1:
            same_stack = True
            c_print('WARNING: One or more tenants are an the same stack.', color='yellow')
            c_print('Some tenant components may not migrate/sync properly. eg Cloud Accounts.', color='yellow')

    return(tenant_sessions, same_stack)

#Read migration settings file
def load_migrate_modes():
    try:
        with open('migrate_mode_settings.json', 'r') as f:
            migrate_modes = json.load(f)
            return migrate_modes
    except:
        c_print('migrate_mode_settings.json not found. Generating...', color='yellow')
        print()
        return {}

#Read sync settings file
def load_sync_modes():
    try:
        with open('sync_mode_settings.json', 'r') as f:
            sync_modes = json.load(f)
            return sync_modes
    except:
        c_print('sync_mode_settings.json not found. Generating...', color='yellow')
        print()
        return {}

if __name__ == '__main__':
    #Load JWT sessions from credentials.yaml
    tenant_sessions, same_stack = load_sessions()

    mode = input('Do you want to MIGRATE or SYNC? (M/S): ')
    print()

    #Select migrate mode or sync mode
    mode = mode.lower() 
    if mode == 'm' or mode == 'migrate':#--------------------------------------------------
        #Optional used saved settings file
        migrate_modes_file = load_migrate_modes()
        if migrate_modes_file:
            choice = input('Do you want to use the saved migration mode settings? (Y/N): ')
            print()
            choice = choice.lower()
            if choice == 'y' or choice == 'yes':
                migrate_main.migrate(tenant_sessions, migrate_modes_file)
                exit()

        #Get migration settings from the user
        migrate_type = input('Do you want to do a full migration? (Y/N): ')
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
            #Dump settings to file
            with open('migrate_mode_settings.json', 'w') as outfile:
                json.dump(migrate_modes, outfile)

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
            
            #Dump settings to file
            with open('migrate_mode_settings.json', 'w') as outfile:
                json.dump(migrate_modes, outfile)

            #Call migrate module
            migrate_main.migrate(migrate_modes)

    else:#---------------------------------------------------------------------------------
        #Optional used saved settings file
        sync_modes_file = load_sync_modes()
        if sync_modes_file:
            choice = input('Do you want to use the saved sync mode settings? (Y/N): ')
            print()
            choice = choice.lower()
            if choice == 'y' or choice == 'yes':
                sync_main.sync(tenant_sessions, sync_modes_file)
                exit()

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
            #Dump settings to file
            with open('sync_mode_settings.json', 'w') as outfile:
                json.dump(sync_modes, outfile)

            sync_main.sync(tenant_sessions, sync_modes)
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

            enabled = input('Do you want to sync Enterprise Settings? (Y/N): ')
            enabled = enabled.lower()
            if enabled == 'y' or enabled =='yes':
                mode_dict = {}
                sync_modes.update(settings=mode_dict)
            else:
                sync_modes.pop('settings')
            print()

            #Dump settings to file
            with open('sync_mode_settings.json', 'w') as outfile:
                json.dump(sync_modes, outfile)


            #Call sync module
            sync_main.sync(tenant_sessions, sync_modes)


        
        

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


