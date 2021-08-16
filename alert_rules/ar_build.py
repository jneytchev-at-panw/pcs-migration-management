from sdk import load_config
from sdk.colors import c_print

'''
call request the source and destination and appends the missing
alert rules to a new list
'''

def call_source(session, logging=False):
    response = session.request("GET", "/v2/alert/rule")
    src_ar = response.json()
    #for testing
    if logging:
        c_print("Source Tenant: ", color='yellow')
        for items in src_ar:
            print(items)
    return src_ar

def call_destination(session, logging=False):
    response = session.request("GET", "/v2/alert/rule")
    dst_ar = response.json()
    #for testing
    if logging:
        c_print(session.tenant, ":", color='yellow')
        for items in dst_ar:
            print(items)
    return dst_ar

#compares both tenant to find the missing alert rule BUILD and append it to a new list
def compare_ar_build(src_ar: list, dst_ar: list):
    new_ar_build = []
    # loops through src_ar (source tenant) to find the missing alert rules
    for item in src_ar:
        # check whether if the key 'policyScanConfigId' is in dst_ar
        if item['scanConfigType'] == 'SHIFTLEFT':
            # if the alert rule is named 'Default Alert Rule', skips it from migrating
            if item['name'] == 'Default Alert Rule' in [key['name'] for key in dst_ar]:
                continue

            if item['name'] not in [key['name'] for key in dst_ar]:
                # prints the value for the key 'policyScanConfigId' and 'name' of the missing value
                c_print("Missing Alert Rules by Name: ", item.get('name'), color='blue')
                # appends the missing values from users_one into new_alerts_rule
                new_ar_build.append(item)

    return new_ar_build

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    #checks whether there are one or more destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            source = call_source(tenant_sessions[0])
            destination = call_destination(tenant_sessions[index])
            compare_ar_build(source, destination)