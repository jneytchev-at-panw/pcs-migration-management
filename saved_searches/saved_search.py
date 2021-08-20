from sdk import load_config

'''
This script POST (uploads) the query query from the source tenant into the destination.
After posting it into recent searches, run the upload_search to SAVE it.
Good luck!
'''


def save_to_destination(session, query: str, time_range: dict):
    data = {
        "query": query,
        "timeRange": time_range
    }

    response = session.request("POST", "/search/config", json=data)

    return upload_search.upload_search_one(session, [response.json()])


if __name__ == "__main__":
    from policy_migrate import upload_search
    tenant_sessions = load_config.load_config_create_sessions()
    time_range = {
            "relativeTimeType": "BACKWARD",
            "type": "relative",
            "value": {
                "amount": 0,
                "unit": "minute"
        }
    }
    data = save_to_destination(tenant_sessions[1], "config from cloud.resource where cloud.type = 'azure' ", time_range)
    print(data)