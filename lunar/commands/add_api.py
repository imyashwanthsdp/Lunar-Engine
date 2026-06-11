from lunar.utils.config import load_config, save_config
from lunar.utils.printer import success, error

def run(args):
    if len(args) < 2:
        error("Usage: lunar add /endpoint METHOD")
        return

    endpoint = args[0]
    method = args[1]

    config = load_config()

    if config is None:
        error("Run lunar init first")
        return

    config["apis"].append({
        "endpoint": endpoint,
        "method": method
    })

    save_config(config)
    success(f"Added API {endpoint} [{method}]")