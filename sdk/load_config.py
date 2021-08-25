from os import path
import re
import yaml
from sdk.session_manager import Session
from sdk.color_print import c_print

def validate_url(url):
    if 'https://' not in url:
        url = 'https://' + url
    
    url = url.replace('app', 'api')

    url = re.sub(r'prismacloud\.io\S*', 'prismacloud.io', url)

    return url

def get_tenant_credentails():
    name = input('Enter tenant name or pseudonym:\n')
    print()
    a_key = input('Enter tenant access key:\n')
    print()
    s_key = input('Enter tenant secret key:\n')
    print()
    url = input('Enter tenant url. (ex: https://app.ca.prismacloud.io):\n')
    print()
    url = validate_url(url)

    return name, a_key, s_key, url

def build_session_dict(name, a_key, s_key, url):
    session_dict = {
        name: {
            'access_key': a_key,
            'secret_key': s_key,
            'api_url': url
            }
    }
    return session_dict


def load_config_create_sessions():
    '''
    Reads config.yml and generates a list of tenants and tokens for those tenants.

    Returns:
    List with the tenants list and the tokens list that corespond with each tenant.
    '''
    #Open and load config file
    if not path.exists('credentials.yml'):
        credentials = []
        #Create credentials yml file
        c_print('No credentials file found. Generating...', color='yellow')
        print()
        c_print('First enter credentials for the source tenant.', color='blue')
        print()
        src_name, src_a_key, src_s_key, src_url = get_tenant_credentails()
        credentials.append(build_session_dict(src_name, src_a_key, src_s_key, src_url))

        c_print('Now enter credentials for the clone tenants that will be managed by this script.', color='blue')
        print()

        while True:
            cln_name, cln_a_key, cln_s_key, cln_url = get_tenant_credentails()
            credentials.append(build_session_dict(cln_name, cln_a_key, cln_s_key, cln_url))
            
            c_print('Do you want to add another managed tenant? (Y/N): ', color='blue')
            choice = input()
            choice = choice.lower()
            print()

            if not (choice == 'y' or choice == 'yes'):
                break

        with open('credentials.yml', 'w') as yml_file:
            for tenant in credentials:
                yaml.dump(tenant, yml_file, default_flow_style=False)

    with open("credentials.yml", "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    #Parse cfg for tenant names and create tokens for each tenant
    tenant_sessions = []
    for tenant in cfg:
        a_key = cfg[tenant]['access_key']
        s_key = cfg[tenant]['secret_key']
        api_url = cfg[tenant]['api_url']

        tenant_sessions.append(Session(tenant, a_key, s_key, api_url))

    return tenant_sessions


if __name__ == '__main__':
    validate_url('https://app.ca.prismacloud.io/home/beans')