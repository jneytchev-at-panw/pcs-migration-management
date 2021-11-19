from cloud_accounts import cld_single_migrate
from account_groups import acc_single_migrate
from resource_lists import rsc_single_migrate
from user_roles import role_single_migrate
from user_profiles import usr_single_migrate
from ip_allow_lists import ip_single_migrate


def single_migrate(tenant_sessions, entity_type, uuid, logger):
    try:
        if 'cloud' == entity_type:
            cld_single_migrate.single_migrate(tenant_sessions, uuid, logger)
    except Exception as error:
        logger.exception(error)

    try:        
        if 'account' == entity_type:
            acc_single_migrate.single_migrate(tenant_sessions, uuid, logger)
    except Exception as error:
        logger.exception(error)

    try:        
        if 'resource' == entity_type:
            rsc_single_migrate.single_migrate(tenant_sessions, uuid, logger)
    except Exception as error:
        logger.exception(error)

    try:    
        if 'role' == entity_type:
            role_single_migrate.single_migrate(tenant_sessions, uuid, logger)
    except Exception as error:
        logger.exception(error)

    try:    
        if 'user' == entity_type:
            usr_single_migrate.single_migrate(tenant_sessions, uuid, logger)
    except Exception as error:
        logger.exception(error)
    
    try:
        if 'ip' == entity_type:
            ip_single_migrate.single_migrate(tenant_sessions,uuid, logger)
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