from sdk.color_print import c_print

def add_alert_rules(session, alert_rules):
    if alert_rules:
        c_print(f'Adding Alert Rules for tenant: \'{session.tenant}\'', color='blue')
        print()

        for alr in alert_rules:
            print('API - Adding Alert Rule')
            session.request("POST", "/alert/rule", json=alr)

    else:
        c_print(f'No Alert Rules to add for tenant: \'{session.tenant}\'', color='yellow')
        print()