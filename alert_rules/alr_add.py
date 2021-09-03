from sdk.color_print import c_print
from tqdm import tqdm

def add_alert_rules(session, alert_rules, logger):
    if alert_rules:
        logger.info(f'Adding Alert Rules for tenant: \'{session.tenant}\'')

        for alr in tqdm(alert_rules, desc='Adding Alert Rules', leave=False):
            logger.debug('API - Adding Alert Rule')
            session.request("POST", "/alert/rule", json=alr)

    else:
        logger.info(f'No Alert Rules to add for tenant: \'{session.tenant}\'')