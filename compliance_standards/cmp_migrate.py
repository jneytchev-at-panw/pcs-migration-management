from compliance_standards import cmp_compare, cmp_get, cmp_add
from sdk.color_print import c_print

def migrate_compliance_standards(tenant_sessions: list):
    '''
    Accepts a list of tenant session objects.

    Gets a list of the top level compliance standards that are missing and migrates
    the missing compliance standard and all its requirements and sections. Does not
    search for and add missing requirements or sections. That is handled in the 
    sync module which does a much more time intensive nested search of all the 
    compliance data accross all tenants
    '''
    #Get complance standards from all tenants
    tenant_compliance_standards_lists = []
    for session in tenant_sessions:
        tenant_compliance_standards_lists.append(cmp_get.get_compliance_standard_list(session))

    #Compare compliance standards
    clone_compliance_standards_to_migrate = cmp_compare.get_compliance_stanadards_to_add(tenant_sessions, tenant_compliance_standards_lists)

    #Get all requirements and sections for each standard. This is a deep nested search and takes some time
    clone_compliance_standards_data = []
    for tenant in clone_compliance_standards_to_migrate:
        tenant_compliance = []
        for standard in tenant:
            standard_dict = {}

            requirements = []
            requirements_data = cmp_get.get_compliance_requirement_list(tenant_sessions[0], standard)

            for requirement in requirements_data:
                requirement_dict = {}
                
                sections = cmp_get.get_compliance_sections_list(tenant_sessions[0], requirement)

                requirement_dict.update(requirement=requirement)
                requirement_dict.update(sections=sections)
                
                requirements.append(requirement_dict)

            standard_dict.update(standard=standard)
            standard_dict.update(requirements=requirements)

            tenant_compliance.append(standard_dict)
        
        clone_compliance_standards_data.append(tenant_compliance)

    #Migrate compliance standards. First migrate over the standards and translate the UUIDs.
    #Then migrate over the requirements and translate the UUIDS. Finnally migrate the sections.
    for index, tenant_standards in enumerate(clone_compliance_standards_data):
        #Migrate compliance standards
        for standard in tenant_standards:
            cmp_add.add_compliance_standard(tenant_sessions[index + 1], standard['standard'])

        #Translate compliance IDs
        clone_standards = cmp_get.get_compliance_standard_list(tenant_sessions[index + 1])
        for i in range(len(tenant_standards)):
            name = tenant_standards[i]['standard']['name']  
            for j in range(len(clone_standards)):
                if clone_standards[j]['name'] == name:
                    new_id = clone_standards[j]['id']
                    tenant_standards[i]['standard'].update(id=new_id)
                    break
        
        #Migrate compliance requirements
        for index2, standard in enumerate(tenant_standards):
            requirements = standard['requirements']
            std_id = standard['standard']['id']
            for requirement in requirements:
                cmp_add.add_requirement_to_standard(tenant_sessions[index + 1], std_id, requirement['requirement'])

            #Translate compliance IDs
            clone_requirements = cmp_get.get_compliance_requirement_list(tenant_sessions[index+1], standard['standard'])
            for i in range(len(requirements)):
                name = requirements[i]['requirement']['name']
                for j in range(len(clone_requirements)):
                    if clone_requirements[j]['name'] == name:
                        new_id = clone_requirements[j]['id']
                        requirements[i]['requirement'].update(id=new_id)
                        break

            #Update requirements list with the list that has the new ids - maybe not needed but easy to do
            tenant_standards[index2].update(requirements=requirements)

            #Migrate sections now that the requirement UUIDs have been updated
            for requirement in requirements:
                req_id = requirement['requirement']['id']
                sections = requirement['sections']
                cmp_add.add_section_to_requirement(tenant_sessions[index+1], req_id, sections)
    
    c_print('Finished migrating compliance standards')

#==============================================================================
#Test code
if __name__ == '__main__':
    from sdk import load_config
    tenant_sessions = load_config.load_config_create_sessions()

    migrate_compliance_standards(tenant_sessions)

        


    





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