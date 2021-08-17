from sdk.color_print import c_print

def add_alert_rules(session, alert_rules):
    if alert_rules:
        c_print('Adding Alert Rules', color='blue')
        print()

        for alr in alert_rules:
            print('API - Adding Alert Rule')
            session.request("POST", "/alert/rule", json=alr)

    else:
        c_print('No Alert Rules to add', color='yellow')
        print()