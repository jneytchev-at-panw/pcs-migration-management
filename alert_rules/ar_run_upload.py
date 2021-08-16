from sdk import load_config
from sdk.colors import c_print
from alert_rules_migrate.ar_run import compare_ar, call_source, call_destination

'''
Call request the account groups from the source and destination.
Compares the id from the missing alert rule in order to migrate using the correct
account groups id.
'''

def source_ag(session):
    response = session.request("GET", "/cloud/group")
    data = response.json()
    src_ag = []
    for items in data:
        src_ag.append(items)

    return src_ag

def destination_ag(session):
    response = session.request("GET", "/cloud/group")
    data = response.json()
    dst_ag = []
    for items in data:
        dst_ag.append(items)

    return dst_ag

#compare the id from the alert rules accountGroups with the destination to append the correct ids
def compare_ag_id(src_ag, dst_ag, session_one, session_two):
    alert_rules_list = compare_ar(call_source(session_one), call_destination(session_two))
    new_ar = []

    for alert in alert_rules_list:
        for src_group in src_ag:
            #validates if the id from the source account group is the same as the ide from the alert rules
            if src_group['id'] in alert['target']['accountGroups']:
                for dst_group in dst_ag:
                    #validates if both tenants account groups name are the same in order to append the correct ids
                    if src_group['name'] == dst_group['name']:
                        alert['target']['accountGroups'].append(dst_group['id'])
                        #validates if the old ids are present in alert and removes them
                        if src_group['id'] in alert['target']['accountGroups']:
                            alert['target']['accountGroups'].remove(src_group['id'])
        new_ar.append(alert)

    return new_ar

#upload the missing alert rules to one or more destination
def upload_ar(source_ag, destination_ag, session_one, session_two):
    new_alert_rules = compare_ag_id(source_ag, destination_ag, session_one, session_two)

    # checks whether the list is empty
    if len(new_alert_rules):
        alert_to_add = []
        for element in new_alert_rules:
            desc = ""
            if "description" in element:
                desc = element['description']
            payload = {
            "name": element["name"],
            "target": element["target"],
            "notifyOnOpen": element["notifyOnOpen"],
            "enabled": element["enabled"],
            "description": desc,
            "policies": element["policies"],
            "policyLabels": element["policyLabels"],
            "policyScanConfigId": element["policyScanConfigId"],
            "scanAll": element["scanAll"]
            }
            alert_to_add.append(payload)
        new_data = []
        for item in range(len(alert_to_add)):
            new_data = alert_to_add[item]

            response = session_two.request("POST", "/alert/rule", json=new_data)
            if response.status_code == 200:
                c_print('API - Migrating alert rule RUN', color='blue')

        return new_data

    # Prints the following string if the list is empty
    else:
        c_print("\nNo Data to Migrate!", color='yellow')
        print()

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    #checks whether there are one or more destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            upload_ar(source_ag(tenant_sessions[0]), destination_ag(tenant_sessions[index]), tenant_sessions[0], tenant_sessions[index])
