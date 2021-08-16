from sdk.color_print import c_print
from compliance_standards import cmp_add, cmp_get #cmp_update ,cmp_delete

def get_compliance_stanadards_to_add(tenant_sessions: object, compliance_standards: list) -> list:
    '''
    Compares the top level compliance standards between tenants and will return a list of 
    standards that are missing from each tenant.
    '''
    
    original_tenant = compliance_standards[0]
    clone_tenants = compliance_standards[1:]

    #Compare the original tenant to the other clone tenants
    clone_tenants_standards_delta = []
    for tenant in clone_tenants:
        standards_delta = []
        for o_cmp_std in original_tenant:
            if o_cmp_std['name'] not in [cmp_std['name'] for cmp_std in tenant]:
                standards_delta.append(o_cmp_std)
        clone_tenants_standards_delta.append(standards_delta)

    #Logging output
    for enum in enumerate(clone_tenants_standards_delta):
        c_print(f'Found {len(enum[1])} compliance standards missing from tenant: {tenant_sessions[enum[0]+1].tenant}.', color='green')
    
    print()

    return clone_tenants_standards_delta

#==============================================================================

def compare_compliance_standards(src_std: dict, cln_std: dict) -> bool:
    '''
    Helper function for syncing compliance data
    '''
    if src_std.get('description', '') != cln_std.get('description', ''):
        return True
    return False

#==============================================================================

def compare_compliance_requirements(src_req: dict, cln_req: dict) -> bool:
    '''
    Helper function for syncing compliance data
    '''
    if src_req['name'] != cln_req['name']:
        return False
    if src_req.get('description', '') != cln_req.get('description', ''):
        return True
    return False

#==============================================================================

def compare_compliance_sections(src_sec: dict, cln_sec: dict):
    '''
    Helper function for syncing compliance data
    '''
    if src_sec['sectionId'] != cln_sec['sectionId']:
        return False
    if src_sec.get('description', '') != cln_sec.get('description', ''):
        return True
    return False

#==============================================================================

#SYNC

# def update_add_delete_compliance_data(source_compliance, clone_compliance, cln_session, addMode, upMode, delMode):
#     '''
#     This function iderates over all the compliance data and will compare then add, update, or delete
#     compliance data from the clone tenant until the clone tenant has the same compliance data as 
#     the source. This function only adds compliance standards that are custom but will update default compliance
#     standards.
#     '''
#     # tenant_compliance = [ 
#     #     {
#     #         'standard': standard_dict,
#     #         'requirements': [
#     #             {
#     #                 'requirement': requirement_dict,
#     #                 'sections': [
#     #                     section_dict
#     #                 ]
#     #             }
#     #             ]
#     #     }
#     # ]
#     #Adding and and updating compliance data
#     for src_cmp_i in range(len(source_compliance)):
#         #Get Compliance Standard to add--------
#         src_cmp_std = source_compliance[src_cmp_i]['standard']
#         if src_cmp_std['name'] not in [cln['standard']['name'] for cln in clone_compliance]:
#             #Add compliance standard to tenant
#             if addMode:
#                 if not src_cmp_std['systemDefault']: #Only add custom
#                     cmp_add.add_compliance_standard(cln_session, src_cmp_std)
#                     #Add sub requirements
#                     cmp_std_id = cmp_get.get_compliance_standard_id_by_name(cln_session, src_cmp_std['name'])
#                     for src_req_data in source_compliance[src_cmp_i]['requirements']:
#                         src_req = src_req_data['requirement']
#                         #Add requirement to tenant
#                         cmp_add.add_requirement_to_standard(cln_session, cmp_std_id, src_req)
#                         #Add sub sections
#                         req_id = cmp_get.get_requirement_id_by_name(cln_session, cmp_std_id, src_req['name'])
#                         for src_sec in src_req_data['sections']:
#                             cmp_add.add_section_to_requirement(cln_session, req_id, src_sec)
        
#         #Get Compliance Standard to update and Requirement Standards to add--------
#         for cln_cmp_i in range(len(clone_compliance)):
#             cln_cmp_data = clone_compliance[cln_cmp_i]
#             src_cmp_data = source_compliance[src_cmp_i]
#             if cln_cmp_data['standard']['name'] == src_cmp_data['standard']['name']:
#                 #Get compliance to updates
#                 if upMode:
#                     if compare_compliance_standards(src_cmp_data['standard'], cln_cmp_data['standard']):
#                         #Update compliance standard
#                         cmp_update.update_compliance_standard(cln_session, cln_cmp_data['standard']['id'], src_cmp_data['standard'])

#                 #Get Requirement Standards to add
#                 src_cmp_req = src_cmp_data['requirements']
#                 for src_req_data in src_cmp_req:
#                     src_req = src_req_data['requirement']
#                     if src_req['name'] not in [cln_req['requirement']['name'] for cln_req in cln_cmp_data['requirements']]:
#                         #Requirement is missing, add requirements to tenant
#                         if addMode:
#                             if not src_req['systemDefault']:#Only add custom
#                                 cmp_std_id = cln_cmp_data['standard']['id']
#                                 cmp_add.add_requirement_to_standard(cln_session, cmp_std_id, src_req)
#                                 #Add sub sections
#                                 req_id = cmp_get.get_requirement_id_by_name(cln_session, cmp_std_id, src_req['name'])
#                                 for src_sec in src_req_data['sections']:
#                                     #Get clone requirement by name 
#                                     cmp_add.add_section_to_requirement(cln_session, req_id, src_sec)
#                     else:
#                         #Get Requirement standards to update and sections to add--------
#                         #Get requirements that need to be updated
#                         cln_cmp_req = cln_cmp_data['requirements']
#                         for cln_req_data in cln_cmp_req:
#                             cln_req = cln_req_data['requirement']
#                             if upMode:
#                                 if compare_compliance_requirements(cln_req, src_req):
#                                     #Update compliance requirement
#                                     cmp_update.update_compliance_requirement(cln_session, cln_req['id'], src_req)

#                         #Get sections that need to be added
#                         cln_req = [cln_req for cln_req in cln_cmp_data['requirements'] if cln_req['requirement']['name'] == src_req['name']][0]
#                         for src_sec in src_req_data['sections']:
#                             if src_sec['sectionId'] not in [sec['sectionId'] for sec in cln_req['sections']]:
#                                 #Section is missing from requirement, add it
#                                 if addMode:
#                                     if not src_sec['systemDefault']: #Only add custom
#                                         cmp_add.add_section_to_requirement(cln_session, cln_req['requirement']['id'], src_sec)
#                             #Compare sections in requirements
#                             if upMode:
#                                 for cln_sec in cln_req['sections']:
#                                     if compare_compliance_sections(src_sec, cln_sec):
#                                         cmp_update.update_compliance_section(cln_session, cln_sec['id'], src_sec)

#     #Deleting compliance data
#     if delMode:
#         for cln_cmp_i in range(len(clone_compliance)):         
#             #Get Compliance Standard to delete--
#             cln_cmp_std = clone_compliance[cln_cmp_i]['standard']
#             if cln_cmp_std['name'] not in [src['standard']['name'] for src in source_compliance]:
#                 #Delete compliance standard from tenant
#                 cmp_delete.delete_compliance_standard(cln_session, cln_cmp_std['id'])

#             for src_cmp_i in range(len(source_compliance)):
#                 cln_cmp_data = clone_compliance[cln_cmp_i]
#                 src_cmp_data = source_compliance[src_cmp_i]
#                 if cln_cmp_data['standard']['name'] == src_cmp_data['standard']['name']:
#                     #Get requirements to delete
#                     cln_cmp_req = cln_cmp_data['requirements']
#                     for cln_req_data in cln_cmp_req:
#                         cln_req = cln_req_data['requirement']
#                         if cln_req['name'] not in [src_req_data['requirement']['name'] for src_req_data in src_cmp_data['requirements']]:
#                             #Delete requirement
#                             cmp_delete.delete_compliance_requirement(cln_session, cln_req['id'])
#                         else:
#                             #Get sections to delete
#                             src_req = [src_req for src_req in src_cmp_data['requirements'] if src_req['requirement']['name'] == cln_req['name']][0]
#                             for cln_sec in cln_req_data['sections']:
#                                 if cln_sec['sectionId'] not in [sec['sectionId'] for sec in src_req['sections']]:
#                                     #Delete section
#                                     cmp_delete.delete_compliance_section(cln_session, cln_sec['id'])
#     return