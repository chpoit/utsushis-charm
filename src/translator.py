import os
import json
import sys
from .resources import get_translation_location, get_language_from_code


class Translator:
    def __init__(self, language="eng"):
        self.load_language(language)
        self.language_code = language
        self.language = get_language_from_code(language)

    def __call__(self, *args, **kwargs):
        return self.get_tl(*args, **kwargs)

    def load_language(self, language):
        lang_file = get_translation_location(language)
        if not os.path.isfile(lang_file):
            raise Exception("Invalid language file")

        with open(lang_file, encoding="utf-8") as f:
            self.translations = json.load(f)

    def get_tl(self, message_key):
        if not message_key in self.translations:
            return message_key
        return self.translations[message_key]
