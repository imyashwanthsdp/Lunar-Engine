import json
import os

CONFIG_FILE = "lunar.config.json"


def init_config(base_url=None, hf_token=None):

    config = {
        "base_url": base_url or "",
        "hf_token": hf_token or "",
        "apis": []
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def load_config():

    if not os.path.exists(CONFIG_FILE):
        return {}

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)