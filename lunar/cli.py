import sys

# Ensure stdout and stderr use UTF-8 encoding to prevent UnicodeEncodeError on Windows
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from lunar.commands import init, add_api, run, generate, config, stress
from lunar.utils.printer import print_banner, print_panel, CYAN, GRAY, RESET, BOLD

def main():
    args = sys.argv[1:]

    if not args:
        print_banner()
        menu_lines = [
            f"{CYAN}{BOLD}init{RESET}            Initialize a new Lunar testing project",
            f"{CYAN}{BOLD}config show{RESET}     Display current project settings",
            f"{CYAN}{BOLD}config set{RESET}      Configure system variables (e.g. hf_token)",
            f"{CYAN}{BOLD}add <url> <m>{RESET}   Register a new API route and HTTP method",
            f"{CYAN}{BOLD}gen <url>{RESET}       Discover schema and generate AI test suite",
            f"{CYAN}{BOLD}run{RESET}             Execute local test scenarios and compile statistics",
            f"{CYAN}{BOLD}stress <url> [n] [c]{RESET} Benchmark latency/throughput under concurrent load",
            f"{CYAN}{BOLD}report{RESET}          Launch the visual high-tech dashboard report",
        ]
        print_panel("AVAILABLE SYSTEM MODULES", menu_lines, border_color=CYAN)
        return

    command = args[0]

    if command == "init":
        init.run()

    elif command == "add":
        add_api.run(args[1:])

    elif command == "run":
        run.run(args[1:])

    elif command == "gen":
        generate.run(args[1:])

    elif command == "report":
        from lunar.commands import report
        report.run(args[1:])

    elif command == "config":
        config.run(args[1:])

    elif command == "stress":
        stress.run(args[1:])

    else:
        print(f"Unknown command: {command}")