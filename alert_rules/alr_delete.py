from sdk.color_print import c_print

def delete_alert_rules(session, alert_rules):
    if alert_rules:
        c_print(f'Deleteing Alert Rules from tenant: \'{session.tenant}\'', color='green')
        print()

        for alert in alert_rules:
            alr_id = alert['policyScanConfigId']
            status_ignore = [201, 204]
            session.request("DELETE", f"/alert/rule/{alr_id}", status_ignore=status_ignore)

    else:
        c_print(f'No Alert Rules to delete from tenant: \'{session.tenant}\'', color='yellow')
        print()