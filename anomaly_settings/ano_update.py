from sdk.color_print import c_print

def update_settings(session: list, settings: list):
    if settings:
        c_print('Updating Anomaly Settings', color='blue')
        print()

        items = settings.items()
        for item in items:
            update_setting(session, item[1], item[0])
    else:
        c_print('No Anomaly Settings to update', color='yellow')
        print()

def update_setting(session: object, plc_id: str, setting: dict):
    c_print(f'API - Updating policy anomaly setting')
    session.request('POST', f'/anomalies/settings/{plc_id}', json=setting)

def add_trusted_list(session: object, trusted_list: dict):
    c_print('API - Adding anomaly trusted list')
    session.request('POST', '/anomalies/trusted_list', json=trusted_list)

def update_trusted_list(session: object, trusted_list: dict):
    ano_id = trusted_list['id']
    print('API - Updating trusted anomaly list')
    session.request('PUT', f'/anomalies/trusted_list/{ano_id}', json=trusted_list)

def delete_trusted_list(session: object, trusted_list: dict):
    ano_id = trusted_list['id']
    print('API - Deleting trusted anomaly list')
    session.request('DELETE', f'/anomalies/trusted_list/{ano_id}')
    