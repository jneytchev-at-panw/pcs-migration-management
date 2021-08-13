from sdk import load_config
from sdk.colors import c_print
from resource_migrate.rl_get import compare_rl, call_source, call_destination

'''
Calls the compare function and migrates the missing resource list
'''

def upload_rl(session_one, session_two):
    new_rl = compare_rl(call_source(session_one), call_destination(session_two))
    # checks whether the list is empty
    if len(new_rl):
        # loops through the list and appends the corresponding parameters to properly migrate the resource list
        rl_to_add = []
        for element in new_rl:
            desc = ""
            if "description" in element:
                desc = element['description']
            payload = {
            "name": element["name"],
            "id": element["id"],
            "description": desc,
            "members": element["members"],
            "resourceListType": element["resourceListType"]
            }
            rl_to_add.append(payload)

        #loops through new_rl and store the data by dictionaries individually
        new_data = []
        for resource in rl_to_add:
            new_data = resource
            #ignores the following request code
            status_ignore = [201]
            response = session_two.request("POST", "/v1/resource_list", json=new_data, status_ignore=status_ignore)

            if response.status_code == 200 or response.status_code == 201:
                c_print('API - Migrating resource list')
        return new_data

    #prints the following string if the list is empty (no data to compare)
    else:
        c_print("\nNo Data to Migrate!", color='yellow')
        print()

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    #checks whether there are one or more destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            upload_rl(tenant_sessions[0], tenant_sessions[index])
