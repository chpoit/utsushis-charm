import os
import json
import sys
from .utils import get_resource_path

class TextFinder():
    def __init__(self, language="en"):
        self.load_language(language)

    def __call__(self, *args, **kwargs):
        return self.get_tl(*args, **kwargs)
    
    def load_language(self, language):
        lang_dir = get_resource_path("TRANSLATIONS")
        lang_file = os.path.join(lang_dir, f"{language}.json")
        if not os.path.isfile(lang_file):
            raise Exception("Invalid language file")
        
        with open(lang_file) as f:
            self.translations = json.load(f)

    def get_tl(self, message_key):
        if not message_key in self.translations:
            return message_key
        return self.translations[message_key]
