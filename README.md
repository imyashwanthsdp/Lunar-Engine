#  Lunar

**AI-Powered API Testing Framework**

Lunar is an intelligent API testing CLI that combines automatic API discovery, AI-generated test cases, automated execution, and rich HTML reporting into a single developer-friendly workflow.

Instead of manually writing API tests, Lunar analyzes your endpoints, understands response schemas, generates meaningful test cases, executes them, and produces visual reports.

---

## ✨ Features

* 🤖 AI-generated API test cases
* 🔍 Automatic endpoint schema discovery
* ⚡ Fast HTTP test execution
* 📊 Beautiful HTML reports
* 🛠 Simple CLI workflow
* 📦 Lightweight and easy to install
* 🔒 Bring your own HuggingFace API token
* 🌐 Works with any REST API

---

## Installation

```bash
pip install lunar-system
```

Verify installation:

```bash
lunar
```

---

## HuggingFace Setup

Lunar uses open-source Large Language Models hosted on HuggingFace to generate intelligent test cases.

### Create a HuggingFace Token

Visit:

https://huggingface.co/settings/tokens

Create a token and copy it.

---

### Windows (PowerShell)

```powershell
$env:HF_TOKEN="your_huggingface_token"
```

### Linux / macOS

```bash
export HF_TOKEN="your_huggingface_token"
```

---

## Quick Start

### 1. Initialize a Lunar Project

```bash
lunar init
```

This creates:

```text
lunar.config.json
```

---

### 2. Configure Your API

Edit:

```json
{
    "base_url": "https://your-api.com",
    "apis": []
}
```

Example:

```json
{
    "base_url": "https://dummyjson.com",
    "apis": []
}
```

---

### 3. Generate Tests

```bash
lunar gen /users
```

Lunar will:

* Discover endpoint schema
* Analyze response structure
* Generate AI-powered test cases
* Save tests automatically

Example output:

```text
✔ Schema discovered

🤖 Generating tests...

✔ Basic status check

✔ Tests saved to lunar_tests/users.json
```

---

### 4. Run Tests

```bash
lunar run
```

Example:

```text
Running tests...

✔ Get all users -> PASS
✔ Status code check
✔ JSON structure check
```

---

### 5. Generate Report

```bash
lunar report
```

Lunar automatically generates:

```text
lunar_reports/report.html
```

and opens the report in your browser.

---


## Example Workflow

```bash
lunar init

lunar gen /users

lunar run

lunar report
```

---

## How Lunar Works

### Schema Discovery

Lunar first inspects the API response to understand:

* Response type
* Status codes
* JSON structure
* Available fields

### AI Test Generation

Using an LLM, Lunar generates:

* Positive test cases
* Edge cases
* Validation checks
* Response assertions

### Test Execution

Generated tests are executed automatically against the target API.

### Reporting

Results are converted into an interactive HTML report for quick analysis.

---

## Requirements

* Python 3.9+
* Internet connection
* HuggingFace API Token

---

## Roadmap

### Current

* AI test generation
* Schema discovery
* Test execution engine
* HTML reporting
* CLI workflow

### Upcoming

* Authentication testing
* Request body generation
* Load testing
* CI/CD integration
* OpenAPI/Swagger support
* Test suites
* Regression testing
* Multi-environment support

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

Feel free to open an issue or submit a pull request.

---

## License

MIT License

---

Built with ❤️ using Python and Open-Source AI.
