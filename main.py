import json
import sys
from loguru import logger
from tqdm import tqdm
from main_scripts import migrate_main, sync_main
from sdk.color_print import c_print
from sdk.load_config import load_config_create_sessions


#Build the dictionary used for sync to determin if the module should support the update, add and delete operations
def build_module():
    module_dict = {}
    full = input('Do you want to use default operations (Add, Update)? (Y/N): ')
    full = full.lower()
    if full =='y' or full =='yes':
        module_dict.update(add=True)
        module_dict.update(update=True)
        module_dict.update(delete=False)
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
            del_2 = input('Deleted entities are not recoverable. Are you sure you want to enable this operation? (Y/N):')
            del_2 = del_2.lower()
            if del_2 == 'y' or del_2 == 'yes':
                module_dict.update(delete=True)
            else:
                module_dict.update(delete=False)
        else:
            module_dict.update(delete=False)

        return module_dict

#Read credentials config file
def load_sessions(file_mode: bool, logger):
    '''
    Returns the tenant sessions, config settings, and a flag for same-stack syncing/migration detected.
    '''

    tenant_sessions = load_config_create_sessions(file_mode, logger)

    tenant_ids = [tenant.prismaId for tenant in tenant_sessions]
    if len(tenant_ids) != len(set(tenant_ids)):
        logger.critical('Duplicate Tenant Detected')
        logger.warning('Make sure source and destination tenants are all unique')
        c_print('Duplicate tenant found. Exiting...', color='red')
        c_print('Make sure your source and destination tenants are all unique.', color='yellow')
        quit()

    tenant_urls = [tenant.api_url for tenant in tenant_sessions]
    same_stack = False
    if len(tenant_urls) != len(set(tenant_urls)):
        logger.warning('Same Stack Detected')
        c_print('WARNING: One or more tenants are an the same stack.', color='yellow')
        c_print('Some tenant components may not migrate/sync properly. eg Cloud Accounts.', color='yellow')
        logger.warning('Some tenant components may not migrate/sync properly. eg Cloud Accounts.')
        same_stack = True

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

@logger.catch
def main(file_mode, logger):
    print()
    c_print('PRISMA CLOUD TENANT MIGRATION AND CENTRAL MANAGEMENT TOOL', color='blue')
    print()

    #Load JWT sessions from credentials.yaml
    tenant_sessions, same_stack = load_sessions(file_mode, logger)

    print()
    c_print('You will now be asked a series of questions so you can customize the operations this script will perform.', color='blue')
    c_print('This script supports two main modes, Migration and Sync.The Migration mode is intended to be used when you', color='blue')
    c_print('are copying data from a full tenant to an empty or mostly empty tenant or tenants. The Sync mode is intended', color='blue')
    c_print('to be used when you want to Add, Update, and Delete elements from one or more clone tenants so that those', color='blue')
    c_print('clone tenants will become identical to your source tenant. The Sync mode does a deep search of all involved', color='blue')
    c_print('tenants so that even the smallest change will be detected and reflected across all managed tenants.', color='blue')
    print()
    print()

    #Run the script based on user responces to the following prompts
    mode = input('Do you want to MIGRATE or SYNC? (M/S): ')
    print()

    #Select migrate mode or sync mode
    mode = mode.lower() 
    if mode == 'm' or mode == 'migrate':#--------------------------------------------------
        #Optional used saved settings file
        migrate_modes_file = load_migrate_modes()
        if migrate_modes_file:
            c_print('Loading from saved settings will allow you to run the script with the same settings as the last time it was ran.', color='blue')
            c_print('If you wish to use the same settings as last time, then select \'Yes\'. If you wish to configure the script to', color='blue')
            c_print('run with new settings, then select \'No\'', color='blue')
            print()
            choice = input('Do you want to use the saved migration mode settings? (Y/N): ')
            print()
            choice = choice.lower()
            if choice == 'y' or choice == 'yes':
                #Call migrate module
                migrate_main.migrate(tenant_sessions, migrate_modes_file, logger)
                return

        #Get migration settings from the user
        c_print('A full migration will migrate all components of the Prisma Cloud Tenant that are supported by this script.', color='blue')
        c_print('Selecting \'No\' will allow you to customize which components are migrated.', color='blue')
        print()
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
            'search': {},
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
            migrate_main.migrate(tenant_sessions, migrate_modes, logger)
            return
        else:
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'cloud')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'account')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'resource')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'role')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'user')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'ip')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'compliance')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'search')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'policy')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'alert')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'anomaly')
            migrate_modes = get_migrate_mode_settings(migrate_modes, 'settings')
            
            #Dump settings to file
            with open('migrate_mode_settings.json', 'w') as outfile:
                json.dump(migrate_modes, outfile)

            #Call migrate module
            migrate_main.migrate(tenant_sessions, migrate_modes, logger)
            return

    else:#---------------------------------------------------------------------------------
        #Optional used saved settings file
        sync_modes_file = load_sync_modes()
        if sync_modes_file:
            c_print('Loading from saved settings will allow you to run the script with the same settings as the last time it was ran.', color='blue')
            c_print('If you wish to use the same settings as last time, then select \'Yes\'. If you wish to configure the script to', color='blue')
            c_print('run with new settings, then select \'No\'', color='blue')
            print()
            choice = input('Do you want to use the saved sync mode settings? (Y/N): ')
            print()
            choice = choice.lower()
            if choice == 'y' or choice == 'yes':
                #Call sync module
                sync_main.sync(tenant_sessions, sync_modes_file, logger)
                return

        c_print('A full sync will do Add and Update operations on all components of the Prisma Cloud Tenant that are supported by this script.', color='blue')
        c_print('Selecting \'No\' will allow you to customize the components that are synced and the operations that are performed.', color='blue')
        print()
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
            sync_main.sync(tenant_sessions, sync_modes, logger)
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
            sync_main.sync(tenant_sessions, sync_modes, logger)
            return


if __name__ =='__main__':
    #Command line arguments
    file_mode = False
    terminal_logging = True
    
    args = [el.lower() for el in sys.argv]

    if '-yaml' in args:
        file_mode = True

    if '-quiet' in args:
        terminal_logging = False

    #Configure logging output
    logger.remove()

    if terminal_logging:
        logger.level("BAR", no=4)
    else:
        logger.level("BAR", no=51)

    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True, level='BAR')
    logger.add('logs/{time:DD-MM-YYYY_HH:mm:ss}.log', level='TRACE')

    #Call main function
    main(file_mode, logger)

    #TODO Maybe run a clean up script and delete credentails files
