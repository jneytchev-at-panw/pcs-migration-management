from sdk.color_print import c_print

def delete_account_groups(session, account_groups, logger):
    if account_groups:
        logger.info(f'Deleting Account Groups from tenant: \'{session.tenant}\'')

        for acc in tqdm(account_groups, desc='Deleteing Account Groups'):
            grp_id = acc.get('id')
            logger.debug('API - Deleteing Account Group')
            session.request('DELETE', f"/cloud/group/{grp_id}")

    else:
        logger.info(f'No Account Groups to delete for tenant: \'{session.tenant}\'')