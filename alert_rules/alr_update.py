from sdk.color_print import c_print

def update_alert_rules(session, alert_rules):
    if alert_rules:
        c_print(f'Updating Alert Rules for tenant: \'{session.tenant}\'', color='green')
        print()

        for alert_rule in alert_rules:
            alr_id = alert_rule['policyScanConfigId']

            print('API - Updating Alert Rule')
            session.request('PUT', f'/alert/rule/{alr_id}', json=alert_rule)
    else:
        c_print(f'No Alert Rule to update for tenant: \'{session.tenant}\'', color='yellow')
        print()