from anomaly_settings import ano_get, ano_update, ano_compare
from sdk.color_print import c_print

def sync(tenant_sessions: list, addMode: bool, upMode: bool, delMode: bool):
        #Get network settings----
    network_settings_list = []
    for session in tenant_sessions:
        data = ano_get.get_all_network_settings(session)
        network_settings_list.append(data)

    #Get settings to update
    settings_to_update = ano_compare.compare_settings(network_settings_list)

    #Update settings
    for index, tenant in enumerate(settings_to_update):
        for n_setting in tenant:
            ano_update.update_setting(tenant_sessions[index + 1], n_setting[0], n_setting[1])
            pass

    #Get UEBA settings----
    ueba_settings_list = []
    for session in tenant_sessions:
        data = ano_get.get_all_ueba_settings(session)
        ueba_settings_list.append(data)
    
    #Get settings to update
    settings_to_update = ano_compare.compare_settings(ueba_settings_list)

    #Update settings
    for index, tenant in enumerate(settings_to_update):
        for n_setting in tenant:
            ano_update.update_setting(tenant_sessions[index + 1], n_setting[0], n_setting[1])
            pass

    #Update settings

    #Get anomaly trusted lists----
    trusted_lists_list = []
    for session in tenant_sessions:
        data = ano_get.get_trusted_lists(session)
        trusted_lists_list.append(data)

    #Getting anomaly lists to add
    trusted_lists_to_add = ano_compare.get_lists_to_add(trusted_lists_list)
    for index, tenant in enumerate(trusted_lists_to_add):
        for t_list in tenant:
            ano_update.add_trusted_list(tenant_sessions[index + 1], t_list)

    #Get anomaly lists to update
    trusted_lists_to_update = ano_compare.get_lists_to_update(trusted_lists_list)
    for index, tenant in enumerate(trusted_lists_to_update):
        for t_list in tenant:
            ano_update.update_trusted_list(tenant_sessions[index + 1], t_list)

    #Get anomaly lists to delete
    trusted_lists_to_delete = ano_compare.get_lists_to_delete(trusted_lists_list)
    for index, tenant in enumerate(trusted_lists_to_update):
        for t_list in tenant:
            ano_update.delete_trusted_list(tenant_sessions[index + 1], t_list)

    c_print('Finished syncing Anomaly Settings', color='blue')
    print()


if __name__ == '__main__':
    from sdk.load_config import load_config_create_sessions

    tenant_sessions = load_config_create_sessions()

    sync(tenant_sessions, True, True, True)