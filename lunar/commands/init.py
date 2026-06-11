from lunar.utils.config import init_config
from lunar.utils.printer import success, error, CYAN, MAGENTA, RESET, BOLD, print_banner

def run():
    print_banner()

    base_url = input(f"{CYAN}{BOLD}[?]{RESET} Enter Base URL (e.g. https://api.example.com): ").strip()

    if not base_url:
        error("Base URL cannot be empty")
        return

    hf_token = input(f"{MAGENTA}{BOLD}[?]{RESET} Enter HuggingFace API Token (optional, press Enter to skip): ").strip()

    init_config(base_url, hf_token)

    success("Lunar project initialized successfully!")