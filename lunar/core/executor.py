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
            body = test.get("body")
            headers = test.get("headers", {})
            query_params = test.get("query_params")

            # Default content-type header for payload transmission
            if body is not None and "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"

            import time
            start_time = time.perf_counter()
            response = requests.request(method, url, json=body, headers=headers, params=query_params)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 1)

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
            # CONTENT TYPE CHECK
            # -----------------------
            expected_content_type = test.get("assertions", {}).get("content_type")
            if expected_content_type is not None:
                actual_content_type = response.headers.get("Content-Type", "")
                if expected_content_type.lower() in actual_content_type.lower():
                    checks.append((f"content_type:{expected_content_type}", True))
                else:
                    checks.append((f"content_type:{expected_content_type}", False))
                    passed = False

            # -----------------------
            # CONTAINS TEXT CHECK
            # -----------------------
            expected_texts = test.get("assertions", {}).get("contains_text", [])
            for expected_text in expected_texts:
                if expected_text.lower() in response.text.lower():
                    checks.append((f"contains_text:{expected_text}", True))
                else:
                    checks.append((f"contains_text:{expected_text}", False))
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
            # JSON TYPES CHECK
            # -----------------------
            expected_types = test.get("assertions", {}).get("json_types", {})
            if expected_types:
                try:
                    data = response.json()
                    for key, exp_type in expected_types.items():
                        if isinstance(data, dict) and key in data:
                            val = data[key]
                            type_mapping = {
                                "str": str, "string": str,
                                "int": int, "integer": int,
                                "float": float, "number": (int, float),
                                "bool": bool, "boolean": bool,
                                "list": list, "array": list,
                                "dict": dict, "object": dict
                            }
                            target_type = type_mapping.get(exp_type.lower())
                            if target_type and isinstance(val, target_type):
                                checks.append((f"type:{key} is {exp_type}", True))
                            else:
                                checks.append((f"type:{key} is {exp_type}", False))
                                passed = False
                        else:
                            checks.append((f"type:{key} is {exp_type}", False))
                            passed = False
                except Exception:
                    checks.append(("json_parse_types", False))
                    passed = False

            # -----------------------
            # JSON VALUES CHECK
            # -----------------------
            expected_values = test.get("assertions", {}).get("json_values", {})
            if expected_values:
                try:
                    data = response.json()
                    for key, exp_val in expected_values.items():
                        if isinstance(data, dict) and key in data:
                            if data[key] == exp_val:
                                checks.append((f"value:{key} == {exp_val}", True))
                            else:
                                checks.append((f"value:{key} == {exp_val}", False))
                                passed = False
                        else:
                            checks.append((f"value:{key} == {exp_val}", False))
                            passed = False
                except Exception:
                    checks.append(("json_parse_values", False))
                    passed = False

            # -----------------------
            # MAX RESPONSE TIME CHECK
            # -----------------------
            max_time = test.get("assertions", {}).get("max_response_time_ms")
            if max_time is not None:
                if duration_ms <= max_time:
                    checks.append((f"latency <= {max_time}ms", True))
                else:
                    checks.append((f"latency <= {max_time}ms (took {duration_ms}ms)", False))
                    passed = False
            # STORE RESULT
            # -----------------------
            results.append({
                "name": test.get("name", "Unnamed Test"),
                "endpoint": test["endpoint"],
                "method": method,
                "status": response.status_code,
                "passed": passed,
                "checks": checks,
                "duration_ms": duration_ms
            })

        except Exception as e:

            results.append({
                "name": test.get("name", "Unnamed Test"),
                "endpoint": test["endpoint"],
                "method": method,
                "status": "ERROR",
                "passed": False,
                "checks": [("request_failed", False)],
                "duration_ms": 0.0
            })

    # -----------------------
    # SAVE REPORT DATA
    # -----------------------
    os.makedirs("lunar_reports", exist_ok=True)

    with open("lunar_reports/latest.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    return results