from user_profiles import usr_get, usr_add

def single_migrate(tenant_sessions, uuid, logger):
    profiles = usr_get.get_users(tenant_sessions[0], logger)

    profile_to_add = {}

    for usr in profiles:
       if usr.get('email') == uuid:
           profile_to_add = usr

    if profile_to_add:
        #translate roles

        for session in tenant_sessions[1:]:
            usr_add.add_users(session, [profile_to_add], logger)
    else:
        logger.warning(f'Could not find User Profile with email \'{uuid}\'')