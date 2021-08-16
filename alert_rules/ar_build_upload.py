from sdk import load_config
from sdk.color_print import c_print
from alert_rules.ar_build import compare_ar_build, call_source, call_destination

'''
Call request the resource list from both tenants and compare its id to the missing alert rule's
targetResourceId to replace in order to migrate with its corresponding resource list. 
'''

def source_rl(session, logging=False):
    response = session.request("GET", "/v1/resource_list")
    data = response.json()
    src_rl = []

    for items in data:
        src_rl.append(items)
    #for testing
    if logging:
        for items in src_rl:
            print(items)
    return src_rl

def destination_rl(session, logging=False):
    response = session.request("GET", "/v1/resource_list")
    data = response.json()
    dst_rl = []

    for items in data:
        dst_rl.append(items)
    #for testing
    if logging:
        for items in dst_rl:
            print(items)
    return dst_rl

#compares the id from the resource list in order to append the correct destination id
#to the missing alert rule
def compare_resource_id(resource_list_src, resource_list_dst, session_one, session_two):
    resource_list = compare_ar_build(call_source(session_one), call_destination(session_two))
    new_rl = []
    #iterates through the missing alert rule to find and replace the targetResourceId
    #with that of the destination resource list id
    for resource in resource_list:
        for src_resource in resource_list_src:
            if src_resource['id'] in resource['target']['targetResourceList']['ids']:
                for dst_resource in resource_list_dst:
                    if src_resource['name'] == dst_resource['name']:
                        resource['target']['targetResourceList']['ids'].append(dst_resource['id'])
                        if src_resource['id'] in resource['target']['targetResourceList']['ids']:
                            resource['target']['targetResourceList']['ids'].remove(src_resource['id'])
        new_rl.append(resource)
    return new_rl

#upload the missing alert rule with its corresponding parameters
def upload_ar_build(src_resource, dst_resource, session_one, session_two):
    new_rl = compare_resource_id(src_resource, dst_resource, session_one, session_two)
    #checks whether the list is empty
    if len(new_rl):
        #iterate through the list to append the corresponding parameters in order to properly POST to the API
        alert_to_add = []
        for element in new_rl:
            desc = ""
            if "description" in element:
                desc = element['description']
            payload = {
            "name": element["name"],
            "target": element["target"],
            "notifyOnOpen": element["notifyOnOpen"],
            "enabled": element["enabled"],
            "policies": element["policies"],
            "description": desc,
            "policyLabels": element["policyLabels"],
            "policyScanConfigId": element["policyScanConfigId"],
            "scanAll": element["scanAll"],
            "scanConfigType": element["scanConfigType"]
            }
            alert_to_add.append(payload)

        #iterates through the alert_to_add and store dictionaries
        new_data = []
        for item in range(len(alert_to_add)):
            new_data = alert_to_add[item]

            response = session_two.request("POST", "/alert/rule", json=new_data)
            if response.status_code == 200:
                c_print('API - Migrating alert rule BUILD', color='blue')

        return new_data

    #Prints the following string if the list is empty (no data to compare)
    else:
        c_print("\nNo Data to Migrate!", color='yellow')
        print()

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    #checks whether there are one or more destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            upload_ar_build(source_rl(tenant_sessions[0]), destination_rl(tenant_sessions[index]), tenant_sessions[0], tenant_sessions[index])
