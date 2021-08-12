def compare_account_groups(src_acc_grps, cln_acc_grps):
    '''
    Compares account groups between the source tenant and a clone tenant.
    Returns the list of account groups missing from the clone tenant
    '''
    acc_grps_to_add = []
    for src_ag in src_acc_grps:
        if src_ag['name'] not in [cln_ag['name'] for cln_ag in cln_acc_grps]:
            acc_grps_to_add.append(src_ag)

    return acc_grps_to_add