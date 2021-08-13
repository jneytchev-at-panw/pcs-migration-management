from sdk.color_print import c_print

def get_roles(session: object):
    c_print('API - Getting roles')
    res = session.request('GET', '/user/role')

    return res.json() 