import json
import os
import time
from lunar.core.executor import run_tests
from lunar.utils.config import load_config
from lunar.utils.printer import (
    success, error, warn, info, print_panel, print_table, print_progress_bar,
    CYAN, MAGENTA, GREEN, RED, YELLOW, BLUE, GRAY, RESET, BOLD
)

def run(args=None):
    config = load_config()
    if not config:
        error("Run lunar init first")
        return

    base_url = config["base_url"]
    test_dir = "lunar_tests"

    if not os.path.exists(test_dir):
        error("No test suite directory ('lunar_tests') discovered. Generate some tests first using: lunar gen <endpoint>")
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
                info(f"Loaded test definitions from {CYAN}{file}{RESET}")
            except Exception as e:
                error(f"Failed to decode test suite {file}: {e}")

    if not all_tests:
        warn("No test cases found in your suite definitions.")
        return

    print(f"\n{CYAN}{BOLD}EXECUTING {len(all_tests)} API TEST SCENARIO(S)...{RESET}\n")

    results = run_tests(base_url, all_tests)

    print(f"\n{CYAN}{BOLD}DETAILED EXECUTION REPORT{RESET}\n")

    passed_count = 0
    total_duration = 0.0

    for idx, r in enumerate(results):
        status_tag = f"{GREEN}{BOLD}PASS{RESET}" if r["passed"] else f"{RED}{BOLD}FAIL{RESET}"
        if r["passed"]:
            passed_count += 1

        duration = r.get("duration_ms", 0.0)
        total_duration += duration

        latency_str = f"{YELLOW}{duration}ms{RESET}"
        status_code_str = f"{BLUE}HTTP {r['status']}{RESET}" if isinstance(r['status'], int) else f"{RED}{r['status']}{RESET}"

        # Display the main test target line
        print(f"[{status_tag}] {BOLD}{r['name']}{RESET}")
        print(f"      {GRAY}→{RESET} {r['method']} {CYAN}{r['endpoint']}{RESET} | {status_code_str} | {latency_str}")

        # Display assertions
        for check, ok in r["checks"]:
            symbol = f"{GREEN}✔{RESET}" if ok else f"{RED}✖{RESET}"
            print(f"        {symbol} {check}")
        print()

    # Calculate statistics
    failed_count = len(results) - passed_count
    success_rate = round((passed_count / len(results)) * 100, 1) if len(results) > 0 else 0.0
    avg_latency = round(total_duration / len(results), 1) if len(results) > 0 else 0.0

    # High tech execution dashboard table
    print(f"\n{CYAN}{BOLD}LUNAR ENGINE SUMMARY DASHBOARD{RESET}\n")
    
    headers = ["METRIC", "VALUE"]
    rows = [
        ["Total Executed", str(len(results))],
        ["Passed Suite", f"{GREEN}{passed_count}{RESET}"],
        ["Failed Suite", f"{RED}{failed_count}{RESET}"],
        ["Success Ratio", f"{CYAN}{BOLD}{success_rate}%{RESET}"],
        ["Avg Latency", f"{YELLOW}{avg_latency} ms{RESET}"],
        ["Total Duration", f"{YELLOW}{round(total_duration/1000, 2)} s{RESET}"],
    ]
    
    print_table(headers, rows)
    print()