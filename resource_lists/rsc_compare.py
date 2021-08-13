def compare_resource_lists(source_resource_lists: list, clone_resource_lists: list):
    '''
    Compare the resource lists between the source tenants and a clone tenant.

    Returns a list of the resource lists that are missing from the clone tenant.
    '''
    
    resource_lists_to_add = []
    for src_rsc in source_resource_lists:
        if src_rsc['name'] not in [cln_rsc['name'] for cln_rsc in clone_resource_lists]:
            resource_lists_to_add.append(src_rsc)

    return resource_lists_to_add