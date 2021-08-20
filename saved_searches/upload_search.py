from sdk import load_config

if __name__ == "__main__":
    from policy_migrate import policy_search
    from policy_migrate import upload_search
    tenant_sessions = load_config.load_config_create_sessions()
    
    saved_search = policy_search.call_leader(tenant_sessions[0])
    call_search = policy_search.call_search(saved_search)
    upload_search.upload_search_one(tenant_sessions[1], call_search)


def upload_search_one(session, search):
    print(search)
    default = 'false'
    if 'default' in search:
        default = search['default']
    desc = ''
    if 'description' in search:
        desc = search['description']
    
    payload = {
        "cloudType": search['cloudType'],
        "default": default,
        "description": desc,
        "id": search['id'],
        "name": search['name'],
        "query": search['query'],
        "saved": search['saved'],
        "timeRange": {
            "relativeTimeType": search['timeRange']['relativeTimeType'],
            "type": search['timeRange']['type'],
            "value": search['timeRange']
            }
        }
    response = session.request("POST", f"/search/history/{'bf08d3ed-4b5d-4613-a6dd-1797f479cfdc'}", json=payload)

    if response.status_code == 200:
        print('Uploaded!')
        return response.json()['id']
    else:
        return 'BAD'
