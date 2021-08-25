from compliance_standards import cmp_compare, cmp_get, cmp_add, cmp_migrate
from sdk.color_print import c_print

def sync(tenant_sessions: list, addMode: bool, upMode: bool, delMode: bool, tenant_compliance_standards_data=[]):
    '''
    Normalizes custom compliance standards accross all tenants using the first tenant as the template
    for the others. Does a deep search accross all tenants to collect all compliance standards, requirements
    and sections so that they can be compared. Compliance data will be added, updated or delted from the clone
    tenants until each clone tenant matches the one source tenant.
    '''
    
    if not tenant_compliance_standards_data:#Sometimes the compliance data is passed in. Mainly used by the delete function
        #Get complance standards from all tenants
        tenant_compliance_standards_lists = []
        for session in tenant_sessions:
            tenant_compliance_standards_lists.append(cmp_get.get_compliance_standard_list(session))

        #Get all requirements and sections for each standard. This is a deep nested search and takes some time  
        for index, tenant in enumerate(tenant_compliance_standards_lists):
            tenant_compliance = []
            for standard in tenant:
                standard_dict = {}

                requirements = []
                requirements_data = cmp_get.get_compliance_requirement_list(tenant_sessions[index], standard)

                for requirement in requirements_data:
                    requirement_dict = {}
                    
                    sections = cmp_get.get_compliance_sections_list(tenant_sessions[index], requirement)

                    requirement_dict.update(requirement=requirement)
                    requirement_dict.update(sections=sections)
                    
                    requirements.append(requirement_dict)

                standard_dict.update(standard=standard)
                standard_dict.update(requirements=requirements)

                tenant_compliance.append(standard_dict)
            
            tenant_compliance_standards_data.append(tenant_compliance)

    #Once the compliance standards have been gathered, get compliance data that needs to be added, updated, and deleted

    source_compliance_standards = tenant_compliance_standards_data[0]
    clone_compliance_standards = tenant_compliance_standards_data[1:]

    #Sync compliance data
    for index, clone in enumerate(clone_compliance_standards):
        session = tenant_sessions[index + 1]
        cmp_compare.update_add_delete_compliance_data(source_compliance_standards, clone, session, addMode, upMode, delMode)


    c_print('Finished syncing Compliance Data', color='blue')
    print()

    return tenant_compliance_standards_data


#==============================================================================
#Test code
if __name__ == '__main__':
    from sdk import load_config
    tenant_sessions = load_config.load_config_create_sessions()

    sync(tenant_sessions, True, True, True)

        


# tenant_compliance = [ 
#     {
#         'standard': standard_dict,
#         'requirements': [
#             {
#                 'requirement': requirement_dict,
#                 'sections': [
#                     section_dict
#                 ]
#             }
#             ]
#     }
# ]