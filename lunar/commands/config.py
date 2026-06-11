from lunar.utils.config import load_config, save_config
from lunar.utils.printer import success, error, print_table, CYAN, RESET, BOLD

def run(args):
    if not args:
        error("Usage: lunar config set <key> <value> OR lunar config show")
        return

    action = args[0]

    config = load_config()
    if not config:
        error("Run lunar init first")
        return

    # SHOW CONFIG
    if action == "show":
        print(f"\n{CYAN}{BOLD}LUNAR SYSTEM CONFIGURATION{RESET}\n")
        headers = ["PARAMETER", "VALUE"]
        rows = []
        for k, v in config.items():
            rows.append([k, str(v)])
        print_table(headers, rows)
        return

    # SET CONFIG
    if action == "set":
        if len(args) < 3:
            error("Usage: lunar config set <key> <value> (e.g., base_url <url> or hf_token <token>)")
            return

        key = args[1]
        value = args[2]

        config[key] = value
        save_config(config)

        success(f"Config parameter '{key}' updated successfully")
        return

    error("Unknown config command")