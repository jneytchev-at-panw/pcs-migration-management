from sdk.color_print import c_print

def delete_compliance_standard(session, cmp_id):
    c_print(f'API - Deleting compliance standard')
    session.request('DELETE', f'/compliance/{cmp_id}')

def delete_compliance_requirement(session, req_id):
    c_print('API - Deleting compliance requirement')
    session.request('DELETE', f'/compliance/requirement/{req_id}')

def delete_compliance_section(session, sec_id):
    c_print('API - Deleting compliance standard')
    session.request('DELETE', f'/compliance/requirement/section/{sec_id}')
