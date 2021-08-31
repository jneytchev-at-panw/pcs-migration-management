from sdk.color_print import c_print
from tqdm import tqdm

def add_resource_lists(session: object, resource_lists_to_add: list, logger):
    tenant_name = session.tenant
    if resource_lists_to_add:
        logger.info(f'Adding Resource Lists to tenant: \'{tenant_name}\'')

        status_ignore = [201]
        for rsc in tqdm(resource_lists_to_add, desc='Adding Resource Lists'):
            logger.debug('API - Adding Resource List')
            session.request('POST', '/v1/resource_list', json=rsc, status_ignore=status_ignore)

    else:
        
        logger.info(f'No Resource Lists to add for tenant: \'{tenant_name}\'')


