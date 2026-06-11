from lunar.utils.config import load_config, save_config
from lunar.utils.printer import success, error

def run(args):
    if not args:
        error("Usage: lunar config set base_url <url> OR lunar config show")
        return

    action = args[0]

    config = load_config()
    if config is None:
        error("Run lunar init first")
        return

    # SHOW CONFIG
    if action == "show":
        print("\n--- CONFIG ---")
        print(config)
        return

    # SET CONFIG
    if action == "set":
        if len(args) < 3:
            error("Usage: lunar config set base_url <url>")
            return

        key = args[1]
        value = args[2]

        config[key] = value
        save_config(config)

        success(f"{key} set to {value}")
        return

    error("Unknown config command")