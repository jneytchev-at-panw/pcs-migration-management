from resource_migrate.rl_upload import upload_rl
from sdk import load_config

'''
calls the upload function to migrate the missing resource list to one or more destination
'''

def rl_main(tenant_sessions, logging=False):
    #checks whether there are one or more destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            upload_rl(tenant_sessions[0], tenant_sessions[index])

#for testing
if __name__ == "__main__":
    tenant_sessions = load_config.load_config_create_sessions()
    logging = False
    # user_input = input("Would like to view the tenants Resource List? y/n: ")
    # if user_input == "y":
    #     logging = True
    # else:
    #     logging = False
    rl_main(tenant_sessions, logging)