from policies import plc_cmp_translate
from saved_searches import search_migrate_plc
from sdk.color_print import c_print

def update_custom_policies(tenant_session: object, source_tenant_session: object, policies: dict):
    if policies:
        c_print(f'Updateing Custom Policies for tenant: \'{tenant_session.tenant}\'', color='green')
        print()

        translate = plc_cmp_translate.Translate(tenant_session)
        for policy in policies:
            p_type = policy['policyType']
            plc_id = policy['policyId']
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

            print(f'API - Updating policy: {name}')
            tenant_session.request('PUT', f'/policy/{plc_id}', policy)
    else:
        c_print(f'No Custom Policies to update for tenant: \'{tenant_session.tenant}\'', color='green')
        print()


def build_compliance_metadata(compliance_metadata, translate):
    modified_compliance_metadata = []
    for el in compliance_metadata:
        if 'complianceId' in el:
            cmp_id = translate.translate_compliance_id(el['standardName'], el['requirementId'], el['sectionId'])
            el.update(complianceId = cmp_id)

            modified_compliance_metadata.append(el)

    return compliance_metadata
