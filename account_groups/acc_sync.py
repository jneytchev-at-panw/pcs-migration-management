from account_groups import acc_get, acc_compare, acc_add, acc_update, acc_delete
from sdk.color_print import c_print

from cross_tenant_translation import create_matrix

def sync(tenant_sessions: list, addMode: bool, upMode: bool, delMode: bool, logger):
    '''
    Accepts a list of tenant sessions objects.

    Adds, Updates, and Deletes account group to sync changes accross all tenants supplied.
    '''

    #Get all account groups
    tenant_acc_grps = []
    for session in tenant_sessions:
        data = acc_get.get_account_groups(session, logger)
        tenant_acc_grps.append(data)

    matrix = create_matrix.create_account_groups_matrix(tenant_acc_grps, tenant_sessions, {})

    src_acc_grps = tenant_acc_grps[0]
    cln_tenant_acc_grps = tenant_acc_grps[1:]

    if addMode:
        #Get account groups to add
        cln_tenant_acc_grps_to_add = []
        for cln_acc_grps in cln_tenant_acc_grps:
            acc_grps = acc_compare.compare_account_groups(src_acc_grps, cln_acc_grps)
            cln_tenant_acc_grps_to_add.append(acc_grps)

        #Add account groups
        for index, cln_acc_grps in enumerate(cln_tenant_acc_grps_to_add):
            session = tenant_sessions[index + 1]
            acc_add.add_account_groups(session, cln_acc_grps, logger)

    if upMode:
        #Get account groups to update
        cln_tenant_acc_grps_to_update = []
        for cln_acc_grps in cln_tenant_acc_grps:
            acc_grps = acc_compare.get_account_groups_to_update(src_acc_grps, cln_acc_grps)
            cln_tenant_acc_grps_to_update.append(acc_grps)

        for index, cln_acc_grps in enumerate(cln_tenant_acc_grps_to_update):
            session = tenant_sessions[index + 1]
            acc_update.update_account_groups(session, cln_acc_grps, logger)

    if delMode:
        cln_tenant_acc_grps_to_delete = []
        for cln_acc_grps in cln_tenant_acc_grps:
            acc_grps = acc_compare.get_account_groups_to_delete(src_acc_grps, cln_acc_grps)
            cln_tenant_acc_grps_to_delete.append(acc_grps)

        for index, cln_acc_grps in enumerate(cln_tenant_acc_grps_to_delete):
            session = tenant_sessions[index + 1]
            acc_delete.delete_account_groups(session, cln_acc_grps, logger)
        

    logger.info('Finished syncing Account Groups')

if __name__ =='__main__':
    from sdk.load_config import load_config_create_sessions

    tenant_session = load_config_create_sessions()

    sync(tenant_session, True, True, True)
    
