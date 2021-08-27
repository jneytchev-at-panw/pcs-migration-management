import json
import sys
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
def load_sessions(file_mode: bool):
    '''
    Returns the tenant sessions, config settings, and a flag for same-stack syncing/migration detected.
    '''

    tenant_sessions = load_config_create_sessions(file_mode)

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

#==============================================================================

def msg_translate(module):
    msg = ''
    if module =='cloud':
        msg = 'Cloud Acccounts'
    elif module == 'account':
        msg = 'Account Groups'
    elif module == 'resource':
        msg ='Resource Lists'
    elif module == 'role':
        msg = 'User Roles'
    elif module == 'user':
        msg = 'User Profiles'
    elif module =='ip':
        msg = 'Trusted IPs'
    elif module == 'compliance':
        msg = 'Compliance Data'
    elif module == 'search':
        msg = 'Saved Searches'
    elif module == 'policy':
        msg = 'Policies'
    elif module == 'alert':
        msg = 'Alert Rules'
    elif module == 'anomaly':
        msg = 'Anomaly Settings'
    elif module == 'settings':
        msg = 'Enterprise Settings'

    return msg

#==============================================================================

def get_migrate_mode_settings(migrate_modes, module):
    msg = msg_translate(module)
    enabled = input(f'Do you want to migrate {msg}? (Y/N): ')
    enabled = enabled.lower()
    if enabled != 'y' and enabled != 'yes':
        migrate_modes.pop(module)
    print()

    return migrate_modes

#==============================================================================

def get_sync_mode_settings(sync_modes, module):
    msg = msg_translate(module)
    enabled = input(f'Do you want to sync {msg}? (Y/N): ')
    enabled = enabled.lower()
    if enabled == 'y' or enabled == 'yes':
        mode_dict = build_module()
        sync_modes[module]=mode_dict
    else:
        sync_modes.pop(module)
    print()

    return sync_modes

#==============================================================================

def main(file_mode):
    #Load JWT sessions from credentials.yaml
    tenant_sessions, same_stack = load_sessions(file_mode)

    #Run the script based on user responces to the following prompts
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
                #Call migrate module
                migrate_main.migrate(tenant_sessions, migrate_modes_file)
                return

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

            #Call migrate module
            migrate_main.migrate(tenant_sessions, migrate_modes)
            return
        else:
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'cloud')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'account')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'resource')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'role')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'user')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'ip')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'compliance')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'policy')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'alert')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'anomaly')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'settings')
            
            #Dump settings to file
            with open('migrate_mode_settings.json', 'w') as outfile:
                json.dump(migrate_modes, outfile)

            #Call migrate module
            migrate_main.migrate(tenant_sessions, migrate_modes)
            return

    else:#---------------------------------------------------------------------------------
        #Optional used saved settings file
        sync_modes_file = load_sync_modes()
        if sync_modes_file:
            choice = input('Do you want to use the saved sync mode settings? (Y/N): ')
            print()
            choice = choice.lower()
            if choice == 'y' or choice == 'yes':
                #Call sync module
                sync_main.sync(tenant_sessions, sync_modes_file)
                return

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

            #Call sync module
            sync_main.sync(tenant_sessions, sync_modes)
            return
        else:
            sync_modes = get_sync_mode_settings(sync_modes, 'cloud')
            sync_modes = get_sync_mode_settings(sync_modes, 'account')
            sync_modes = get_sync_mode_settings(sync_modes, 'resource')
            sync_modes = get_sync_mode_settings(sync_modes, 'role')
            sync_modes = get_sync_mode_settings(sync_modes, 'user')
            sync_modes = get_sync_mode_settings(sync_modes, 'ip')
            sync_modes = get_sync_mode_settings(sync_modes, 'compliance')
            sync_modes = get_sync_mode_settings(sync_modes, 'search')
            sync_modes = get_sync_mode_settings(sync_modes, 'policy')
            sync_modes = get_sync_mode_settings(sync_modes, 'alert')
            sync_modes = get_sync_mode_settings(sync_modes, 'anomaly')
            sync_modes = get_sync_mode_settings(sync_modes, 'settings')

            #Dump settings to file
            with open('sync_mode_settings.json', 'w') as outfile:
                json.dump(sync_modes, outfile)

            #Call sync module
            sync_main.sync(tenant_sessions, sync_modes)
            return


if __name__ =='__main__':
    file_mode = False
    
    #Read command line args
    if 'fileMode' in sys.argv:
        file_mode = True
    
    main(file_mode)

    #TODO Maybe run a clean up script and delete credentails files
