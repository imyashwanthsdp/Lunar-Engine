#  Lunar

**AI-Powered High-Tech API Testing & Performance Benchmarking CLI Framework**

Lunar is an intelligent, developer-first command-line tool designed to completely automate the testing, validation, and performance benchmarking of REST APIs and web endpoints. 

It combines automated schema discovery, AI-powered multi-method test suite generation, advanced response assertions (validating status codes, content types, JSON schemas, field data types, values, and response latency limits), multithreaded stress benchmarking, and rich visual HTML dashboards into a single high-tech command-line workflow.

---

##  Features

* 🤖 **AI-Generated Test Suites**: Instantly generates complete API lifecycles (GET, POST, PUT, DELETE, PATCH) with realistic mock payloads matching your endpoint structure.
* ⚡ **Performance Benchmarking (`lunar stress`)**: Runs concurrent threads using Python thread pools to profile throughput (RPS) and latency percentiles (p50, p90, p95, p99) with real-time progress bars.
* 🔍 **Schema Discovery (JSON & HTML)**: Probes endpoints to extract JSON keys, data types, HTML titles, content-type headers, and body text previews.
* 🛠 **Advanced Assertion Engine**: Validates status codes, content types, text presence (`contains_text`), JSON keys (`json_keys`), field data types (`json_types`), exact field values (`json_values`), and latency thresholds (`max_response_time_ms`).
* 📊 **High-Tech Dashboard Reports**: Compiles test execution histories into premium, dark-mode visual HTML dashboards and launches them in your browser.
* 🔒 **Configurable Tokens**: Support for HuggingFace Hub client credentials loaded dynamically from environment variables or project config files.
* 🖥 **Futuristic CLI UX**: High-contrast cyberpunk console output utilizing unicode panels, aligned grid tables, and color badges.

---

## Installation

Install the Lunar CLI from the Python Package Index (PyPI):

```bash
pip install lunar-engine
```

Verify your installation:

```bash
lunar
```

---

## Quick Start Guide

### 1. Initialize a Lunar Project
Run the following command to start a new project in your current working directory:

```bash
lunar init
```
This launches an interactive prompt setting up:
- **Base URL** (e.g. `https://dummyjson.com` or `https://google.com`)
- **HuggingFace Access Token** *(Optional, used for the test generation AI)*

It initializes your project configuration file: `lunar.config.json`.

---

### 2. View and Update Configuration
Show your current settings in a formatted table:

```bash
lunar config show
```

Update any setting (like changing your API base URL or adding your HuggingFace token):

```bash
lunar config set base_url https://api.example.com
lunar config set hf_token your_huggingface_api_token
```

---

### 3. Generate Tests (AI-Powered)
Generate a test suite for a resource endpoint:

* **Generate a complete CRUD lifecycle suite** (GET list, POST create, PUT update, DELETE remove, negative GET/PUT 404s) containing mock payloads and data validations:
  ```bash
  lunar gen /users
  ```

* **Generate tests targeting a specific HTTP Method**:
  ```bash
  lunar gen /users POST
  ```

Lunar will analyze the live response, map the schema (JSON properties or HTML text), compile the test cases, and save them to `lunar_tests/users.json`.

---

### 4. Execute the Test Suite
Run all tests compiled inside your `lunar_tests/` directory:

```bash
lunar run
```
This executes all request scenarios, formats the assertions inside execution blocks, profiles response times, and outputs a detailed stats dashboard.

---

### 5. Benchmark Performance Concurrency (`lunar stress`)
Benchmark any endpoint under a concurrent request load:

```bash
lunar stress /users [requests_count] [concurrency_level]
```
*Example (100 total requests, 20 concurrent threads)*:
```bash
lunar stress /users 100 20
```
Outputs:
- Total execution duration (seconds)
- System throughput (Requests Per Second, RPS)
- Performance latency percentiles: Median (`p50`), `p90`, `p95`, and `p99` thresholds
- Status code distribution counts and ratios

---

### 6. Compile HTML Visual Reports
Build and compile your visual testing history:

```bash
lunar report
```
This generates a responsive HTML dashboard report at `lunar_reports/report.html` and launches it in your browser.

---

## CLI Command Map Reference

| Command | Usage | Description |
|---|---|---|
| `lunar` | `lunar` | Displays the console banner and command menu panel. |
| `lunar init` | `lunar init` | Interactively initializes project configurations. |
| `lunar config show` | `lunar config show` | Renders active configuration settings in a grid table. |
| `lunar config set` | `lunar config set <key> <val>` | Sets or overrides project settings (e.g. `hf_token`). |
| `lunar add` | `lunar add <endpoint> <method>` | Manually registers an endpoint route. |
| `lunar gen` | `lunar gen <endpoint> [METHOD]` | Probes schemas and compiles AI-generated test suites. |
| `lunar run` | `lunar run` | Executes all local test files and prints assertion audits. |
| `lunar stress` | `lunar stress <url> [reqs] [threads]` | Runs concurrency latency & throughput stress tests. |
| `lunar report` | `lunar report` | Compiles execution history into HTML dashboard reports. |

---

## Advanced Assertion Config Example
Generated test case JSON definitions (saved in `lunar_tests/`) support advanced structures that can be custom edited:

```json
[
    {
        "name": "Verify successful update of user details",
        "endpoint": "/users/1",
        "method": "PUT",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer token"
        },
        "query_params": {
            "dry_run": "false"
        },
        "body": {
            "username": "jane_doe",
            "email": "jane@example.com"
        },
        "assertions": {
            "status_code": 200,
            "content_type": "application/json",
            "contains_text": ["jane_doe"],
            "json_keys": ["id", "username", "email"],
            "json_types": {
                "id": "int",
                "username": "string",
                "email": "string"
            },
            "json_values": {
                "username": "jane_doe"
            },
            "max_response_time_ms": 1500
        }
    }
]
```

---

## Requirements

* Python 3.8+
* Active Internet connection (for schema discovery and AI generation)
* HuggingFace Access Token (to fetch and call model inference)

---

## License

MIT License
