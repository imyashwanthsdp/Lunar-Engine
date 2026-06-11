import requests
import json
import os
from urllib.parse import urljoin


def build_url(base_url, endpoint):

    # If endpoint is already full URL
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        return endpoint

    # Safe join (fixes // issues)
    return urljoin(base_url + "/", endpoint.lstrip("/"))


def run_tests(base_url, tests):

    results = []

    for test in tests:

        url = build_url(base_url, test["endpoint"])
        method = test.get("method", "GET").upper()

        try:
            response = requests.request(method, url)

            passed = True
            checks = []

            # -----------------------
            # STATUS CODE CHECK
            # -----------------------
            expected_status = test.get("assertions", {}).get("status_code")

            if expected_status is not None:
                if response.status_code == expected_status:
                    checks.append(("status_code", True))
                else:
                    checks.append(("status_code", False))
                    passed = False

            # -----------------------
            # JSON KEY CHECK
            # -----------------------
            try:
                data = response.json()
                expected_keys = test.get("assertions", {}).get("json_keys", [])

                for key in expected_keys:
                    if isinstance(data, dict) and key in data:
                        checks.append((f"key:{key}", True))
                    else:
                        checks.append((f"key:{key}", False))
                        passed = False

            except Exception:
                if test.get("assertions", {}).get("json_keys"):
                    checks.append(("json_parse", False))
                    passed = False

            # -----------------------
            # STORE RESULT
            # -----------------------
            results.append({
                "name": test.get("name", "Unnamed Test"),
                "endpoint": test["endpoint"],
                "method": method,
                "status": response.status_code,
                "passed": passed,
                "checks": checks
            })

        except Exception as e:

            results.append({
                "name": test.get("name", "Unnamed Test"),
                "endpoint": test["endpoint"],
                "method": method,
                "status": "ERROR",
                "passed": False,
                "checks": [("request_failed", False)]
            })

    # -----------------------
    # SAVE REPORT DATA
    # -----------------------
    os.makedirs("lunar_reports", exist_ok=True)

    with open("lunar_reports/latest.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    return results