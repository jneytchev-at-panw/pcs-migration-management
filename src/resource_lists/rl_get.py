from sdk import load_config
from sdk.colors import c_print

'''
Call request the source and destination tenants and compares
the missing resource list.
'''

def call_source(session, logging=False):
    print('API - Getting resource list')
    response = session.request("GET", "/v1/resource_list")
    src_rl = response.json()
    #for testing
    if logging:
        c_print(session.tenant, ":", color='yellow')
        for element in src_rl:
            print(element)
    return src_rl

def call_destination(session, logging=False):
    print('API - Getting resource list')
    response = session.request("GET", "/v1/resource_list")
    dst_rl = response.json()
    #for testing
    if logging:
        c_print(session.tenant, ":", color='yellow')
        for element in dst_rl:
            print(element)
    return dst_rl

#compares both tenants to find the missing resource list
def compare_rl(src_rl: list, dst_rl: list):
    new_rl = []
    # loops through alerts_rule_one (source tenant) to find the missing alert rules
    for resource in src_rl:
        # check whether if the key 'policyScanConfigId' is in alerts_rule_two
        if resource['name'] not in [key['name'] for key in dst_rl]:
            # prints the JSON key 'policyScanConfigId' and 'name' of the missing value
            c_print("Missing Resource List: ", resource.get('name'), color='blue')
            #appends the missing resource list from the source
            new_rl.append(resource)

    print()
    
    return new_rl

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    #checks whether there are one or more destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            source = call_source(tenant_sessions[0])
            destination = call_destination(tenant_sessions[index])
            compare_rl(source, destination)