from lunar.core.http_client import send_request
from lunar.core.assertions import run_assertions

def run_tests(base_url, apis):
    results = []

    for api in apis:
        url = base_url + api["endpoint"]
        method = api["method"]
        assertions = api.get("assertions", {})

        try:
            response = send_request(method, url)

            assertion_results = run_assertions(response, assertions)

            passed = all(result[1] for result in assertion_results)

            results.append({
                "endpoint": api["endpoint"],
                "status": response.status_code,
                "assertions": assertion_results,
                "success": passed
            })

        except Exception:
            results.append({
                "endpoint": api["endpoint"],
                "status": "error",
                "assertions": [],
                "success": False
            })

    return results