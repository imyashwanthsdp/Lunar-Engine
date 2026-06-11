from lunar.utils.config import init_config
from lunar.utils.printer import success

def run():

    base_url = input("Enter Base URL (e.g. https://api.example.com): ").strip()

    if not base_url:
        print("❌ Base URL cannot be empty")
        return

    init_config(base_url)

    success("Lunar project initialized")