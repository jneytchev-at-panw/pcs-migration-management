from alert_rules_migrate.ar_run_upload import upload_ar, source_ag, destination_ag
from alert_rules_migrate.ar_build_upload import upload_ar_build, source_rl, destination_rl
from sdk import load_config

'''
call the upload functions for both RUN and BUILD alert rules to migrate to the destination
'''

def alert_rules(tenant_sessions, logging=False):
    #checks whether there are one or more destination
    for index in range(len(tenant_sessions)):
        if index >= 1:
            upload_ar(source_ag(tenant_sessions[0]), destination_ag(tenant_sessions[index]), tenant_sessions[0], tenant_sessions[index])
            upload_ar_build(source_rl(tenant_sessions[0]), destination_rl(tenant_sessions[index]), tenant_sessions[0], tenant_sessions[index])

#for testing
if __name__ == "__main__":
    logging = False
    tenant_sessions = load_config.load_config_create_sessions()
    # user_input = input("Would like to view the tenants alert rules? y/n: ")
    # if user_input == "y":
    #     logging = True
    # else:
    #     logging = False
    alert_rules(tenant_sessions, logging)