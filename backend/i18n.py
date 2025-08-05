import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "locales"
_translations = {}

for lang_file in LOCALES_DIR.glob("*.json"):
  with open(lang_file, 'r', encoding='utf-8') as f:
    _translations[lang_file.stem] = json.load(f)


def translate(lang: str, key: str, **kwargs) -> str:
  lang_dict = _translations.get(lang, _translations.get("en", {}))
  text = lang_dict.get(key, key)
  try:
    return text.format(**kwargs)
  except Exception:
    return text
