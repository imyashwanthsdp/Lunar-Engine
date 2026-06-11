def check_status_code(response, expected):
    return response.status_code == expected


def check_json_keys(data, expected_keys):
    if not isinstance(data, dict):
        return False

    return all(key in data for key in expected_keys)


def run_assertions(response, assertions):
    results = []

    # STATUS CODE CHECK
    if "status_code" in assertions:
        ok = check_status_code(response, assertions["status_code"])
        results.append(("status_code", ok))

    # JSON KEY CHECK
    if "json_keys" in assertions:
        try:
            data = response.json()
        except:
            data = None

        ok = check_json_keys(data, assertions["json_keys"])
        results.append(("json_keys", ok))

    return results