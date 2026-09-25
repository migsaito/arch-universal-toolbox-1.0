import json
import os

class I18n:
    def __init__(self):
        self.locales_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locales")
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        for lang in ["EN-US", "PT-BR", "DE"]:
            file_path = os.path.join(self.locales_dir, f"{lang}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
            else:
                self.translations[lang] = {}

    def get_translation(self, lang):
        return self.translations.get(lang, self.translations.get("EN-US", {}))

i18n = I18n()
translations = i18n.translations
