import json
import os
from lunar.core.executor import run_tests
from lunar.utils.config import load_config


def run(args=None):

    config = load_config()

    base_url = config["base_url"]

    test_dir = "lunar_tests"

    if not os.path.exists(test_dir):
        print("✖ No lunar_tests directory found")
        return

    all_tests = []

    for file in os.listdir(test_dir):

        if file.endswith(".json"):

            file_path = os.path.join(test_dir, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tests = json.load(f)

                    if isinstance(tests, list):
                        all_tests.extend(tests)

                print(f"✔ Loaded {file}")

            except Exception as e:
                print(f"✖ Failed to load {file}: {e}")

    if not all_tests:
        print("✖ No tests found")
        return

    print(f"\n🚀 Running {len(all_tests)} test(s)...\n")

    results = run_tests(base_url, all_tests)

    print("\n--- TEST RESULTS ---\n")

    passed = 0

    for r in results:

        status = "PASS" if r["passed"] else "FAIL"

        if r["passed"]:
            passed += 1

        print(f"{r['name']} -> {status} ({r['status']})")

        for check, ok in r["checks"]:
            symbol = "✔" if ok else "✖"
            print(f"   {symbol} {check}")

        print()

    print("===================================")
    print(f"Passed: {passed}")
    print(f"Failed: {len(results) - passed}")
    print(f"Total : {len(results)}")
    print("===================================")