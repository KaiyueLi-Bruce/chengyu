import json
import random
import sys
from pathlib import Path

from .config import get_default_language, set_api_key, set_default_language, get_api_key, setup, SUPPORTED_LANGUAGES, validate_api_key
from .translator import translate

DATA_PATH = Path(__file__).parent / "data" / "chengyu.json"
PRELOAD_PATH = Path.home() / ".chengyu" / "next.json"

def get_random_chengyu():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return random.choice(data)

def preload_next(lang: str):
    chengyu = get_random_chengyu()
    word = chengyu.get("word", "")
    pinyin = chengyu.get("pinyin", "")
    explanation = chengyu.get("explanation", "")
    example = chengyu.get("example", "")

    translated_explanation = translate(explanation, lang)
    translated_example = translate(example, lang) if example else ""

    preloaded = {
        "word": word,
        "pinyin": pinyin,
        "explanation": translated_explanation,
        "example": translated_example,
        "lang": lang,
    }

    PRELOAD_PATH.parent.mkdir(exist_ok=True) 
    with open(PRELOAD_PATH, "w", encoding="utf-8") as f:
        json.dump(preloaded, f, ensure_ascii=False, indent=2)

def load_preloaded():
    if not PRELOAD_PATH.exists():
        return None
    with open(PRELOAD_PATH, encoding="utf-8") as f:
        return json.load(f)

def print_preloaded(chengyu: dict):
    print()
    print(f"  {chengyu['word']}  ({chengyu['pinyin']})")
    print()
    print(f"  Explanation: {chengyu['explanation']}")
    example = chengyu.get("example", "")
    if example and example != "无" and example != "not have":
        print(f"  Example:     {chengyu['example']}")
    print()

def print_chengyu_live(chengyu: dict, lang: str):
    word = chengyu.get("word", "")
    pinyin = chengyu.get("pinyin", "")
    explanation = chengyu.get("explanation", "")
    example = chengyu.get("example", "")

    translated_explanation = translate(explanation, lang)
    translated_example = translate(example, lang) if example else ""

    print()
    print(f"  {word}  ({pinyin})")
    print()
    print(f"  Explanation: {translated_explanation}")
    example = chengyu.get("example", "")
    if example and example != "无" and example != "not have":
        print(f"  Example:     {translated_example}")
    print()

def is_first_run():
    return not PRELOAD_PATH.exists()

def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("Usage: chengyu [language] [--setup] [--change <language>] [--help]")
        print()
        print("  chengyu                        Show next chengyu in default language")
        print("  chengyu japanese               Show a chengyu in japanese this time only")
        print("  chengyu --setup                Configure API key and default language")
        print("  chengyu --change japanese      Change default language to japanese")
        print("  chengyu --add-key              Add or update your DeepL API key")
        print()
        print(f"  Supported languages: {', '.join(SUPPORTED_LANGUAGES.keys())}")
        return

    # Block normal usage on first run, but allow setup and add-key.
    if is_first_run() and "--setup" not in args and "--add-key" not in args:
        print("Welcome to Chengyu CLI!")
        print("Looks like this is your first time. Let's get you set up first.")
        print()
        setup()
        print()
        print("Preloading first chengyu...")
        preload_next(get_default_language())
        print("All done! Run 'chengyu' again to get your first chengyu.")
        return

    if "--setup" in args:
        setup()
        print()
        print("Preloading first chengyu...")
        preload_next(get_default_language())
        print("Ready! Run 'chengyu' to get started.")
        return

    if "--add-key" in args:
        print("Get a free DeepL API key at: https://www.deepl.com/pro-api")
        api_key = input("Paste your DeepL API key here: ").strip()
        print("  Validating API key...")
        if validate_api_key(api_key):
            set_api_key(api_key)
            print("API key saved!")
        else:
            print("Invalid API key, please try again.")
        return
    
    if "--change" in args:
        idx = args.index("--change")
        if idx + 1 >= len(args):
            print("Error: please provide a language after --change.")
            print("Example: chengyu --change japanese")
            sys.exit(1)
        new_lang = args[idx + 1].lower()
        if new_lang not in SUPPORTED_LANGUAGES:
            print(f"Error: unsupported language '{new_lang}'.")
            print(f"Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}")
            sys.exit(1)

        # Check API key if switching to non-Chinese
        if new_lang != "chinese" and not get_api_key():
            print(f"A DeepL API key is required to use {new_lang}.")
            print("Run 'chengyu --add-key' to configure your API key.")
            sys.exit(1)

        set_default_language(new_lang)
        print(f"Default language changed to {new_lang}.")
        print("Retranslating preloaded chengyu...")
        preload_next(new_lang)
        print("Done!")
        return

    # Override language for this run only
    if args:
        lang = args[0].lower()
        if lang not in SUPPORTED_LANGUAGES:
            print(f"Unsupported language '{lang}'.")
            print(f"Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}")
            sys.exit(1)
        if lang != "chinese" and not get_api_key():
            print(f"A DeepL API key is required to use {lang}.")
            print("Run 'chengyu --add-key' to configure your API key.")
            sys.exit(1)
        try:
            chengyu = get_random_chengyu()
            print_chengyu_live(chengyu, lang)
        except RuntimeError as e:
            print(f"Error: {e}")
            sys.exit(1)
        return

    # Normal run: show preloaded, then preload next
    try:
        current = load_preloaded()
        print_preloaded(current)
        preload_next(get_default_language())
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)