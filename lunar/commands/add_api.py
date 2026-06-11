from lunar.utils.config import load_config, save_config
from lunar.utils.printer import success, error

def run(args):
    if len(args) < 2:
        error("Usage: lunar add /endpoint METHOD")
        return

    endpoint = args[0]
    method = args[1]

    config = load_config()

    if not config:
        error("Run lunar init first")
        return

    if "apis" not in config:
        config["apis"] = []

    config["apis"].append({
        "endpoint": endpoint,
        "method": method
    })

    save_config(config)
    success(f"Added API {endpoint} [{method}]")