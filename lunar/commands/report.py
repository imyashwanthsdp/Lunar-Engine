import json
import os
import webbrowser


def run(args):
    file_path = "lunar_reports/latest.json"

    if not os.path.exists(file_path):
        print("❌ No report found. Run a test first using: lunar run")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        print(f"❌ Error reading latest JSON report: {e}")
        return

    total = len(results)
    passed = len([r for r in results if r.get("passed")])
    failed = total - passed
    pass_percentage = round((passed / total * 100), 1) if total > 0 else 0

    # High-tech, ultra-modern dark theme dashboard template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lunar Test Report</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #0B0F19;
            --bg-card: #131A2C;
            --border-color: #1F293D;
            --text-main: #F3F4F6;
            --text-muted: #9CA3AF;
            --accent-pass: #10B981;
            --accent-pass-glow: rgba(16, 185, 129, 0.15);
            --accent-fail: #EF4444;
            --accent-fail-glow: rgba(239, 68, 68, 0.15);
            --accent-blue: #3B82F6;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            padding: 40px 20px;
            line-height: 1.5;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }}

        h1 {{
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #FFF 0%, #9CA3AF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .timestamp {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: var(--text-muted);
            background: #111827;
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}

        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 40px;
        }}

        .metric-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 20px;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }}

        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; width: 4px; height: 100%;
            background: var(--accent-blue);
        }}

        .metric-card.pass-card::before {{ background: var(--accent-pass); }}
        .metric-card.fail-card::before {{ background: var(--accent-fail); }}

        .metric-label {{
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-bottom: 6px;
        }}

        .metric-value {{
            font-size: 32px;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Test Cards */
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-muted);
        }}

        .test-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .test-card:hover {{
            transform: translateY(-2px);
            border-color: #2D3A54;
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
            margin-bottom: 14px;
        }}

        .test-title {{
            font-size: 18px;
            font-weight: 600;
            color: #FFF;
        }}

        .badge {{
            font-size: 12px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.5px;
        }}

        .badge.pass {{
            color: var(--accent-pass);
            background-color: var(--accent-pass-glow);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .badge.fail {{
            color: var(--accent-fail);
            background-color: var(--accent-fail-glow);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}

        .meta-group {{
            display: flex;
            gap: 16px;
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 16px;
        }}

        .meta-item b {{
            color: var(--text-main);
        }}

        /* Codeblock styling */
        pre {{
            background-color: #070A12;
            border: 1px solid var(--border-color);
            padding: 16px;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            overflow-x: auto;
            color: #E5E7EB;
        }}
    </style>
</head>
<body>

<div class="container">
    <header>
        <div>
            <h1>Lunar Engine Test Report</h1>
        </div>
        <div class="timestamp">LUNAR REPORT ENGINE v1.0</div>
    </header>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-label">Total Executed</div>
            <div class="metric-value">{total}</div>
        </div>
        <div class="metric-card pass-card">
            <div class="metric-label">Passed Suite</div>
            <div class="metric-value" style="color: var(--accent-pass);">{passed}</div>
        </div>
        <div class="metric-card fail-card">
            <div class="metric-label">Failed Suite</div>
            <div class="metric-value" style="color: var(--accent-fail);">{failed}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Success Rate</div>
            <div class="metric-value">{pass_percentage}%</div>
        </div>
    </div>

    <div class="section-title">Execution Logs</div>
"""

    for r in results:
        is_passed = r.get("passed")
        status_label = "PASSED" if is_passed else "FAILED"
        badge_class = "pass" if is_passed else "fail"

        # Safe extraction of response properties
        test_name = r.get("name", "Unnamed Test Execution")
        status_code = r.get("status", "N/A")
        method = r.get("method", "UNKNOWN")
        endpoint = r.get("endpoint", "UNKNOWN")
        checks_json = json.dumps(r.get("checks", []), indent=2)

        html += f"""
    <div class="test-card">
        <div class="card-header">
            <div class="test-title">{test_name}</div>
            <span class="badge {badge_class}">{status_label}</span>
        </div>
        <div class="meta-group">
            <div class="meta-item"><b>Method:</b> {method}</div>
            <div class="meta-item"><b>Route:</b> {endpoint}</div>
            <div class="meta-item"><b>Response Code:</b> {status_code}</div>
        </div>
        <pre><code>{checks_json}</code></pre>
    </div>
"""

    html += """
</div>
</body>
</html>"""

    # Directory Management & Output Writing
    os.makedirs("lunar_reports", exist_ok=True)
    report_path = os.path.abspath("lunar_reports/report.html")

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✔ Report compiled successfully: {report_path}")

        # Instantly open up the fresh report in user's default browser
        webbrowser.open("file://" + report_path)
    except Exception as e:
        print(f"❌ Failed to write or launch HTML report file: {e}")