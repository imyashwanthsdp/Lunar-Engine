import json
import os

from lunar.core.ai import generate_tests
from lunar.core.discovery import discover_schema
from lunar.utils.config import load_config


def normalize_tests(tests):

    # If AI returned a JSON string
    if isinstance(tests, str):
        try:
            tests = json.loads(tests)
        except Exception:
            print("✖ AI returned invalid JSON")
            return []

    # If AI wrapped tests inside an object
    if isinstance(tests, dict):

        # Common wrapper keys
        for key in ["tests", "test_cases", "cases", "data"]:
            if key in tests and isinstance(tests[key], list):
                return tests[key]

        # First list found in dict
        for value in tests.values():
            if isinstance(value, list):
                return value

        return []

    # Already a list
    if isinstance(tests, list):
        return tests

    return []


def run(args):

    if len(args) == 0:
        print("Usage: lunar gen <endpoint>")
        return

    endpoint = args[0]
    method = "GET"

    config = load_config()

    print(f"🔍 Discovering schema for {endpoint}...")

    schema = discover_schema(
        config["base_url"],
        endpoint,
        method
    )

    print("✔ Schema discovered")
    print(schema)

    print(f"\n🤖 Generating tests for {endpoint}...\n")

    raw_tests = generate_tests(
        endpoint,
        method,
        schema
    )

    tests = normalize_tests(raw_tests)

    if not tests:
        print("✖ No valid tests generated")
        print("\nRaw AI Output:")
        print(raw_tests)
        return

    os.makedirs("lunar_tests", exist_ok=True)

    filename = endpoint.strip("/")

    if not filename:
        filename = "root"

    filepath = f"lunar_tests/{filename}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            tests,
            f,
            indent=4
        )

    print("\n--- GENERATED TESTS ---\n")

    for test in tests:

        if not isinstance(test, dict):
            print(f"⚠ Skipping invalid test: {test}")
            continue

        print(f"✔ {test.get('name', 'Unnamed Test')}")
        print(
            f"   → {test.get('method', 'GET')} "
            f"{test.get('endpoint', endpoint)}"
        )
        print(
            f"   → assertions: "
            f"{test.get('assertions', {})}"
        )
        print()

    print(f"✔ Tests saved to {filepath}")