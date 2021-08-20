from sdk.color_print import c_print

def update_login_ips(tenant_session, ips, dst_ips):
    for ip in ips:
        name = ip['name']
        #Translate ID
        l_id = ''
        if name in [i['name'] for i in dst_ips]:
            l_id = [i['id'] for i in dst_ips if i['name'] == name][0]
        ip.pop('id')
        ip.pop('lastModifiedTs')
        c_print('API - Update login allow IP')
        tenant_session.request('PUT', f'/ip_allow_list_login/{l_id}', json=ip)