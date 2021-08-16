from sdk import load_config
from sdk.colors import c_print

'''
call request the source and destination alert rules. Compare both tenants and append 
the missing alert rules to a new list
'''

def call_source(session, logging=False):
    response = session.request("GET", "/v2/alert/rule")
    src_ar = response.json()
    #for testing
    if logging:
        c_print(session.tenant, ":", color='yellow')
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

#compare the tenants to find the missing alert rule
def compare_ar(src_ar: list, dst_ar: list):
    new_ar = []
    # loops through src_ar (source tenant) to find the missing alert rules
    for item in src_ar:
        # skips alert rule named 'Default Alert Rule'
        if item['name'] == 'Default Alert Rule' in [key['name'] for key in dst_ar]:
            continue
        #check if the key 'name' is in both tenants. If not, appends the missing alert rule to a new list
        if item['scanConfigType'] == 'STANDARD':
            if item['name'] not in [key['name'] for key in dst_ar]:
                # prints the value of key 'policyScanConfigId' and 'name' of the missing value
                c_print("Missing Alert Rules by Name: ", item.get('name'), color='blue')
                # appends the missing values from src_ar
                new_ar.append(item)

    return new_ar

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    #checks whether there are more than one destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            source = call_source(tenant_sessions[0])
            destination = call_destination(tenant_sessions[index])
            compare_ar(source, destination)