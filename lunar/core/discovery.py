import requests


def discover_schema(base_url, endpoint, method="GET"):

    url = base_url + endpoint

    response = requests.request(method, url)

    try:
        data = response.json()
    except:
        return {
            "status_code": response.status_code,
            "type": "non-json",
            "keys": []
        }

    if isinstance(data, list):

        if len(data) > 0 and isinstance(data[0], dict):
            keys = list(data[0].keys())
        else:
            keys = []

        return {
            "status_code": response.status_code,
            "type": "array",
            "keys": keys
        }

    if isinstance(data, dict):
        return {
            "status_code": response.status_code,
            "type": "object",
            "keys": list(data.keys())
        }

    return {
        "status_code": response.status_code,
        "type": str(type(data)),
        "keys": []
    }