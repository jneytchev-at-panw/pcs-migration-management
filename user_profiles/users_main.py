from users_migrate.users_upload import upload_users
from sdk import load_config

'''
Calls the upload function to migrate the missing user/s to one ore more destination
'''

def users_main(tenant_sessions):
    #checks whether there are more than one destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            upload_users(tenant_sessions[0], tenant_sessions[index], tenant_sessions[index])

#for testing
if __name__ == "__main__":
    logging = False
    tenant_sessions = load_config.load_config_create_sessions()

    users_main(tenant_sessions)
