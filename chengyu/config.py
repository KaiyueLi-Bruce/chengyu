import json
from pathlib import Path

import requests

CONFIG_DIR = Path.home() / ".chengyu"
CONFIG_FILE = CONFIG_DIR / "config.json"
SUPPORTED_LANGUAGES = {
    "chinese": None,
    "english": "EN",
    "japanese": "JA",
    "french": "FR",
    "german": "DE",
    "spanish": "ES",
    "italian": "IT",
    "korean": "KO",
    "portuguese": "PT",
    "russian": "RU",
    "dutch": "NL",
    "polish": "PL",
}

def ensure_config_dir():
    CONFIG_DIR.mkdir(exist_ok=True)

def get_api_key():
    ensure_config_dir()
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, encoding="utf-8") as f:
        config = json.load(f)
    return config.get("deepl_api_key")

def get_default_language():
    if not CONFIG_FILE.exists():
        return "chinese"
    with open(CONFIG_FILE, encoding="utf-8") as f:
        config = json.load(f)
    return config.get("default_language", "chinese")

def set_api_key(api_key: str):
    ensure_config_dir()
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
    config["deepl_api_key"] = api_key
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def set_default_language(lang: str):
    ensure_config_dir()
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
    config["default_language"] = lang
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def validate_api_key(api_key: str) -> bool:
    try:
        response = requests.get(
            "https://api-free.deepl.com/v2/usage",
            headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
            timeout=5
        )
        return response.status_code == 200
    except requests.RequestException:
        return False
    
def setup():
    print("Chengyu CLI Setup")
    print()
    print("Supported languages: chinese, english, japanese, french, german,")
    print("                     spanish, italian, korean, portuguese, russian, dutch, polish")
    print("A DeepL API key is required for non-Chinese output.")
    while True:
        lang = input("Set your default language (press Enter for chinese): ").strip().lower()
        if not lang:
            lang = "chinese"
        if lang in SUPPORTED_LANGUAGES:
            break
        print(f"  '{lang}' is not a supported language, please try again.")

    if lang != "chinese":
        print()
        print("A DeepL API key is required for non-Chinese output.")
        print("Get one at: https://www.deepl.com/pro-api (choose Free plan)")
        while True:
            api_key = input("Paste your DeepL API key here: ").strip()
            print("  Validating API key...")
            if validate_api_key(api_key):
                set_api_key(api_key)
                print("  API key is valid!")
                break
            else:
                print("  Invalid API key, please try again.")
        print(f"\nAll set! Default language set to {lang}.")
    else:
        print("All set! No API key needed for Chinese output.")