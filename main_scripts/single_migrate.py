from cloud_accounts import cld_single_migrate


def single_migrate(tenant_sessions, entity_type, uuid, logger):
    try:
        if 'cloud' == entity_type:
            cld_single_migrate.single_migrate(tenant_sessions, uuid, logger)
    except Exception as error:
        logger.exception(error)

    try:        
        if 'account' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)

    try:        
        if 'resource' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)

    try:    
        if 'role' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)

    try:    
        if 'user' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)
    
    try:
        if 'ip' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)
    
    try:
        if 'compliance' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)
    
    try:
        if 'search' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)

    try:
        if 'policy' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)

    try:   
        if 'alert' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)

    try:    
        if 'anomaly' == entity_type:
            pass
    except Exception as error:
        logger.exception(error)