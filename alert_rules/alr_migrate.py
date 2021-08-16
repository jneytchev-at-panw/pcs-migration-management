from alert_rules import alr_get, alr_compare, alr_add

def migrate(tenant_sessions):
    '''
    Accepts a list of tenant session.

    For each tenant_session, migrates all alert rules
    '''

    #Get all alert rules
    tenant_alert_rules = []
    for session in tenant_sessions:
        alerts = alr_get.get_alert_rules(session)
        tenant_alert_rules.append(alerts)

    #Get alert rules to add

    #Translte IDs in alert rules

    #Add alert rules

    