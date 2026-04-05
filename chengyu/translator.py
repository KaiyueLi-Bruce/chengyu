import requests
from .config import get_api_key

DEEPL_URL = "https://api-free.deepl.com/v2/translate"
REQUEST_TIMEOUT_SECONDS = 10

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

def translate(text: str, target_lang: str = "chinese") -> str:
    lang = target_lang.lower()

    if lang not in SUPPORTED_LANGUAGES:
        supported = ", ".join(SUPPORTED_LANGUAGES.keys())
        raise ValueError(f"Unsupported language '{target_lang}'. Supported: {supported}")

    if lang == "chinese":
        return text

    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("No API key found. Run 'chengyu --setup' to configure.")

    try:
        response = requests.post(
            DEEPL_URL,
            headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
            json={
                "text": [text],
                "source_lang": "ZH",
                "target_lang": SUPPORTED_LANGUAGES[lang],
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise RuntimeError("Failed to reach DeepL API. Please check your network and try again.") from exc

    if response.status_code != 200:
        raise RuntimeError(f"DeepL API error: {response.status_code} {response.text}")

    return response.json()["translations"][0]["text"]