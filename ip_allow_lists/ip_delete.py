from sdk.color_print import c_print

def delete_login_ips(session, ips, dst_ips):
    if ips:
        c_print(f'Deleting Trusted Login IPs from tenant: \'{session.tenant}\'', color='green')
        print()

        for ip in ips:
            name = ip['name']
            #Translate ID
            l_id = ''
            if name in [i['name'] for i in dst_ips]:
                l_id = [i['id'] for i in dst_ips if i['name'] == name]
            c_print('API - Update login allow IP', color='blue')
            session.request('DELETE', f'/ip_allow_list_login/{l_id}')
    else:
        c_print(f'No Trusted Login IPs to delete for tenant: \'{session.tenant}\'', color='yellow')
        print()
