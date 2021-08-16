from sdk.color_print import c_print
from policies import plc_cmp_translate
from saved_searches import search_migrate_plc

def add_custom_policies(tenant_session, source_tenant_session, policies):
    '''
    Accepts a clone tenant session object, a source tenant session object, and a list of policies to add.

    Adds the custom policies to the first tenant supplied.
    '''

    #Updates IDs and saves searches before adding each policy to the new tenant.

    translate = plc_cmp_translate.Translate(tenant_session)
    
    for policy in policies:
        p_type = policy['policyType']
        name = policy['name']
        desc = name
        if 'description' in policy:
            desc = policy['description']

        #the saved search needs to be migrated if there is one
        if 'savedSearch' in policy['rule']['parameters']:
            savedSearch = policy['rule']['parameters']['savedSearch']
            if savedSearch == 'true' or savedSearch == True or savedSearch =='True' or savedSearch:
                criteria = search_migrate_plc.migrate_search(tenant_session, source_tenant_session, policy['rule'], policy['name'], desc)
                policy['rule'].update(criteria=criteria)

        #The ID of the compliance standards needs to be updated if there is compliance data
        if 'complianceMetadata' in policy:
            complianceMetadata = build_compliance_metadata(policy['complianceMetadata'], translate)
            policy.update(complianceMetadata=complianceMetadata)

        c_print(f'API - Adding {p_type} policy: {name}')
        tenant_session.request('POST', '/policy', json=policy)

def update_default_policy(tenant_session: object, policy: dict):
    '''
    Accepts a tenant session and a built in policy.

    Updates the built in policy.
    '''

    translate = plc_cmp_translate.Translate(tenant_session)

    plc_id = policy['policyId']
    name = policy['name']

    #The ID of the compliance standards needs to be updated if there is compliance data
    if 'complianceMetadata' in policy:
        complianceMetadata = build_compliance_metadata(policy['complianceMetadata'], translate)
        policy.update(complianceMetadata=complianceMetadata)

    c_print(f'API - Updating policy: {name}')
    tenant_session.request('PUT', f'/policy/{plc_id}', policy)

#==============================================================================

def build_compliance_metadata(compliance_metadata: dict, translate: object):
    '''
    Accepts compliance metadata and a translate object.

    Builds up compliance metadata with translated IDs.
    '''
    modified_compliance_metadata = []
    for el in compliance_metadata:
        if 'complianceId' in el:
            cmp_id = translate.translate_compliance_id(el['standardName'], el['requirementId'], el['sectionId'])
            el.update(complianceId = cmp_id)

            modified_compliance_metadata.append(el)

    return compliance_metadata

#==============================================================================

if __name__ == '__main__':
    from sdk import load_config
    tenant_sessions = load_config.load_config_create_sessions()

    event_policy = [{'policyId': 'f6cfa762-0d6a-4a59-85d4-5bb66534cdb8', 'name': 'bwade test', 'policyType': 'audit_event', 'policySubTypes': ['audit'], 'systemDefault': False, 'description': '', 'severity': 'low', 'rule': {'name': 'bwade test', 'criteria': '7b6b0df6-3849-4681-a2b7-167ad7977ed7', 'parameters': {'savedSearch': 'true'}, 'type': 'AuditEvent'}, 'recommendation': '', 'cloudType': 'all', 'labels': [], 'enabled': True, 'createdOn': 1567179247854, 'createdBy': 'bwade@paloaltonetworks.com', 'lastModifiedOn': 1567179647287, 'lastModifiedBy': 'bwade@paloaltonetworks.com', 'ruleLastModifiedOn': 1567179647287, 'deleted': False, 'owner': 'PANW-dev', 'policyMode': 'custom', 'policyCategory': 'incident', 'policyClass': 'privileged_activity_monitoring', 'remediable': False}]

    add_custom_policies(tenant_sessions[1], event_policy)