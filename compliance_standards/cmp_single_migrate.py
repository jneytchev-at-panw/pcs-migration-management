from compliance_standards import cmp_add, cmp_get
from tqdm import tqdm

def single_migrate(tenant_sessions, uuid, logger):
    cmp_type = input('Migrate Compliance Standard, Requirement, or Section. (STD, REQ, SEC): ')

    cmp_type = cmp_type.lower()

    source_session = tenant_sessions[0]

    

    if cmp_type == 'std':
        cmp_to_add = {}
        res = source_session.request('GET', f'/compliance/{uuid}')
        cmp_to_add = res.json()

        #Add compliance
    elif cmp_type == 'req':
        req_to_add = {}
        res = source_session.request('GET', f'/compliance/requirement/{uuid}')
        req_to_add = res.json()

        #Add req
    else:
        tenant_compliance_standards_lists = []
        for session in tenant_sessions:
            tenant_compliance_standards_lists.append(cmp_get.get_compliance_standard_list(session, logger))

        tenant_compliance_standards_data = []
        #Get all requirements and sections for each standard. This is a deep nested search and takes some time
        for index in range(len(tenant_compliance_standards_lists)):
            tenant = tenant_compliance_standards_lists[index]
            tenant_compliance = []
            for standard in tqdm(tenant, desc=f'Getting Compliance Data from Tenant {tenant_sessions[index].tenant}', leave=False):
                standard_dict = {}

                requirements = []
                requirements_data = cmp_get.get_compliance_requirement_list(tenant_sessions[index], standard, logger)

                for requirement in requirements_data:
                    requirement_dict = {}
                    
                    sections = cmp_get.get_compliance_sections_list(tenant_sessions[index], requirement, logger)

                    requirement_dict.update(requirement=requirement)
                    requirement_dict.update(sections=sections)
                    
                    requirements.append(requirement_dict)

                standard_dict.update(standard=standard)
                standard_dict.update(requirements=requirements)

                tenant_compliance.append(standard_dict)
            
            tenant_compliance_standards_data.append(tenant_compliance)
        
        source_compliance_standards = tenant_compliance_standards_data[0]

        cmp_to_add = {}
        req_to_add = {}
        sec_to_add = {}


        for std in source_compliance_standards:
            if std['standard'].get('id') == uuid:
                logger.error('Standard found instead of section')
            else:
                for req in std['requirements']:
                    if req['requirement'].get('id') == uuid:
                        logger.error('Requirement found instead of section')
                    else:
                        for sec in req['standards']:
                            if sec.get('id') == uuid:
                                cmp_to_add = std['standard']
                                req_to_add = req['requirement']
                                sec_to_add = sec

        #Add section


        print(cmp_to_add)