from sdk.color_print import c_print

def migrate_settings(tenant_sessions):
    c_print('API - Getting enterprise settings')
    res = tenant_sessions[0].request('GET', '/settings/enterprise')
    
    settings = res.json()

    if 'userAttributionInNotification' not in settings:
        settings.update(userAttributionInNotification=False)

    clone_tenant_sessions = tenant_sessions[1:]
    for session in clone_tenant_sessions:
        c_print('API - Updating enterprise settings')
        session.request('POST', '/settings/enterprise', json=settings)

    c_print('Finished syncing Enterprise Settings', color='yellow')
    print()

if __name__ == '__main__':
    from sdk.load_config import load_config_create_sessions

    tenant_sessions = load_config_create_sessions()

    migrate_settings(tenant_sessions)