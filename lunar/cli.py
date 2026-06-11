import sys
from lunar.commands import init, add_api, run, generate, config

def main():
    args = sys.argv[1:]

    if not args:
        print("Lunar CLI - commands: init | add | run | gen | config")
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

    else:
        print(f"Unknown command: {command}")