import time
import os
import requests
import concurrent.futures
from lunar.utils.config import load_config
from lunar.utils.printer import (
    success, error, warn, info, print_panel, print_table, print_progress_bar,
    CYAN, MAGENTA, GREEN, RED, YELLOW, BLUE, GRAY, RESET, BOLD
)

def single_request(url, method="GET"):
    start = time.perf_counter()
    try:
        response = requests.request(method, url, timeout=10)
        duration = (time.perf_counter() - start) * 1000
        return response.status_code, duration
    except Exception as e:
        duration = (time.perf_counter() - start) * 1000
        return "ERROR", duration

def run(args):
    if len(args) == 0:
        error("Usage: lunar stress <endpoint> [requests] [concurrency]")
        return

    endpoint = args[0]
    
    # Defaults
    total_requests = 100
    concurrency = 10

    if len(args) > 1:
        try:
            total_requests = int(args[1])
        except ValueError:
            warn(f"Invalid requests count '{args[1]}'. Defaulting to 100.")

    if len(args) > 2:
        try:
            concurrency = int(args[2])
        except ValueError:
            warn(f"Invalid concurrency level '{args[2]}'. Defaulting to 10.")

    config = load_config()
    if not config:
        error("Run lunar init first")
        return

    base_url = config["base_url"]
    
    # Safe join URLs
    if not base_url.endswith("/") and not endpoint.startswith("/"):
        url = base_url + "/" + endpoint
    else:
        url = base_url + endpoint

    print_panel(
        "PERFORMANCE BENCHMARK RUNNER",
        [
            f"{CYAN}Target Endpoint:{RESET} {url}",
            f"{CYAN}Total Requests:{RESET}  {total_requests}",
            f"{CYAN}Concurrency:{RESET}     {concurrency} threads",
        ],
        border_color=CYAN
    )

    info("Executing performance benchmark load tests...")

    durations = []
    status_codes = {}
    completed = 0

    start_bench = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit all tasks
        futures = [executor.submit(single_request, url) for _ in range(total_requests)]
        
        for future in concurrent.futures.as_completed(futures):
            status, duration = future.result()
            durations.append(duration)
            status_codes[status] = status_codes.get(status, 0) + 1
            completed += 1
            
            # Print progress bar
            print_progress_bar(completed, total_requests)

    total_bench_time = time.perf_counter() - start_bench

    # Calculations
    durations.sort()
    
    p50 = round(durations[int(completed * 0.50)] if completed > 0 else 0.0, 1)
    p90 = round(durations[int(completed * 0.90)] if completed > 0 else 0.0, 1)
    p95 = round(durations[int(completed * 0.95)] if completed > 0 else 0.0, 1)
    p99 = round(durations[int(completed * 0.99)] if completed > 0 else 0.0, 1)

    min_latency = round(durations[0] if completed > 0 else 0.0, 1)
    max_latency = round(durations[-1] if completed > 0 else 0.0, 1)
    avg_latency = round(sum(durations) / completed if completed > 0 else 0.0, 1)
    
    throughput_rps = round(completed / total_bench_time, 1) if total_bench_time > 0 else 0.0

    print(f"\n{CYAN}{BOLD}BENCHMARK METRICS SUMMARY{RESET}\n")
    
    metric_headers = ["METRIC", "VALUE"]
    metric_rows = [
        ["Total Time Elapsed", f"{round(total_bench_time, 3)} s"],
        ["Throughput", f"{CYAN}{BOLD}{throughput_rps} RPS{RESET}"],
        ["Min Latency", f"{min_latency} ms"],
        ["Avg Latency", f"{avg_latency} ms"],
        ["Max Latency", f"{max_latency} ms"],
        ["Median (p50) Latency", f"{YELLOW}{p50} ms{RESET}"],
        ["p90 Latency", f"{YELLOW}{p90} ms{RESET}"],
        ["p95 Latency", f"{YELLOW}{p95} ms{RESET}"],
        ["p99 Latency", f"{RED}{BOLD}{p99} ms{RESET}"],
    ]
    print_table(metric_headers, metric_rows)

    print(f"\n{CYAN}{BOLD}RESPONSE STATUS CODES DISTRIBUTION{RESET}\n")
    status_headers = ["STATUS CODE", "COUNT", "RATIO"]
    status_rows = []
    for code, count in sorted(status_codes.items(), key=lambda x: str(x[0])):
        ratio = round((count / completed) * 100, 1)
        color = GREEN if isinstance(code, int) and code < 400 else RED
        status_rows.append([f"{color}{code}{RESET}", str(count), f"{ratio}%"])
    print_table(status_headers, status_rows)
    print()
    
    success("Performance benchmark testing successfully completed.")
