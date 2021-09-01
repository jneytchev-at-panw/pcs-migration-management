from sdk.color_print import c_print
from tqdm import tqdm

def update_login_ips(session, ips, dst_ips, logger):
    if ips:
        logger.info(f'Updating Login IPs for tenant: \'{session.tenant}\'')

        for ip in tqdm(ips, desc='Updating Login IPs', leave=False):
            name = ip['name']
            #Translate ID
            l_id = ''
            if name in [i['name'] for i in dst_ips]:
                l_id = [i['id'] for i in dst_ips if i['name'] == name][0]
            ip.pop('id')
            ip.pop('lastModifiedTs')
            logger.debug('API - Update login allow IP')
            session.request('PUT', f'/ip_allow_list_login/{l_id}', json=ip)
    else:
        logger.debug(f'No Login IPs to update for tenant: \'{session.tenant}\'')
