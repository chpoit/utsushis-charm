from distutils.command.config import config
import os
import sys
import shutil
import platform
from pathlib import Path
from symspellpy.symspellpy import SymSpell
import logging
import json

from .updater.SimpleSemVer import SimpleSemVer

from .exceptions.MissingTranslationError import MissingTranslationError

logger = logging.getLogger(__name__)


HOME = str(Path.home())
WINDOWS = platform.system() == "Windows"
LINUX = platform.system() == "Linux"
MAC = platform.system() == "Darwin"


def get_all_skills(lang="eng"):
    all_skills = {}
    skill_file = os.path.join(get_resource_path("LOCAL_SKILLS"), f"skills.{lang}.txt")
    if not os.path.isfile(skill_file):
        internal = os.path.join(
            get_resource_path("INTERNAL_SKILLS"), f"skills.{lang}.txt"
        )
        shutil.copy(internal, skill_file)

    with open(skill_file, encoding="utf-8") as slf:
        for line in slf.readlines():
            skill_name = line.strip()
            all_skills[skill_name.lower()] = skill_name
    return all_skills


def get_word_freqs_location(lang="eng"):
    freq_file = os.path.join(get_resource_path("LOCAL_SKILLS"), f"skills.{lang}.freq")
    if not os.path.isfile(freq_file):
        internal = os.path.join(
            get_resource_path("INTERNAL_SKILLS"), f"skills.{lang}.freq"
        )
        shutil.copy(internal, freq_file)
    return freq_file


def get_resource_path(resource):
    return _resources[resource] if resource in _resources else resource


def _alter_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_language_list():
    return _language_list


def get_language_code(language: str):
    return _language_code_mappings[language.strip()]


def get_language_from_code(language_code: str):
    return _reverse_language_code_mappings[language_code.strip()]


def _backup_corrections(language_code):
    backup_corr = {}
    all_skills = get_all_skills()
    for skill in all_skills.values():
        for word in skill.split():
            backup_corr[word] = word

    return backup_corr


def load_corrections(language_code, known_corrections=None):
    try:
        known_corrections = known_corrections or {}
        corrections_path = get_corrections_path(language_code)

        with open(corrections_path, encoding="utf-8") as scf:
            known_corrections = {
                w: c for w, c in map(lambda x: x.strip().split(","), scf.readlines())
            }

        return known_corrections
    except FileNotFoundError as e:
        logger.exception("Had to load backup corrections")
        return _backup_corrections(language_code)


def get_spell_checker(language_code):
    spell = SymSpell(max_dictionary_edit_distance=4)
    spell.load_dictionary(
        get_word_freqs_location(language_code), 0, 1, encoding="utf-8"
    )
    return spell


def add_corrections(language_code, known_corrections, *new_tuples):
    corrections_path = get_corrections_path(language_code)
    with open(corrections_path, "a", encoding="utf-8") as c_fp:
        for a, b in new_tuples:
            if not a in known_corrections:
                known_corrections[a] = b
                c_fp.write(f"{a},{b}\n")
    return known_corrections


def get_corrections_path(language_code):
    local_file = os.path.join(
        get_resource_path("LOCAL_DIR"), f"corrections.{language_code}.csv"
    )
    if not os.path.isfile(local_file):
        packaged_corrections = os.path.join(
            get_resource_path("INTERNAL_SKILLS"), f"corrections.{language_code}.csv"
        )
        shutil.copy(packaged_corrections, local_file)
    return local_file


def get_update_url():
    url = "https://raw.githubusercontent.com/chpoit/utsushis-charm/master/data/versions.json"
    return url


def get_lastest_api_url():
    url = "https://api.github.com/repos/chpoit/utsushis-charm/releases/latest"
    return url


def get_latest_url():
    url = "https://github.com/chpoit/utsushis-charm/releases/latest"
    return url


def get_language_url(language="eng"):
    url = f"https://raw.githubusercontent.com/chpoit/utsushis-charm/master/data/translations/{language}.json"
    return url


def get_corrections_url(language="eng"):
    url = f"https://raw.githubusercontent.com/chpoit/utsushis-charm/master/data/skills/corrections.{language}.csv"
    return url


def get_english_skill_mapping_url(language="eng"):
    url = f"https://raw.githubusercontent.com/chpoit/utsushis-charm/master/data/skills/skill_mappings.en.json"
    return url


def get_wiki_url(skill_language_code):
    if skill_language_code == "jpn":
        return "https://mhrise.wiki-db.com/sim"
    return "https://mhrise.wiki-db.com/sim/?hl=en"


def get_english_skill_mappping_location():
    return os.path.join(get_resource_path("LOCAL_SKILLS"), "skill_mappings.en.json")


def get_translation_location(language="eng", for_creation=False):
    local_file = os.path.join(
        get_resource_path("LOCAL_TRANSLATIONS"), f"{language}.json"
    )
    os.makedirs(get_resource_path("LOCAL_TRANSLATIONS"), exist_ok=True)
    
    if not os.path.isfile(local_file) and not for_creation:
        lang_dir = get_resource_path("INTERNAL_TRANSLATIONS")
        lang_file = os.path.join(lang_dir, f"{language}.json")
        if not os.path.isfile(lang_file):
            raise MissingTranslationError(get_language_from_code(language))
        shutil.copy(lang_file, local_file)
    return local_file


def get_versions_location():
    version_file = get_resource_path("versions")
    if not os.path.exists(version_file):
        shutil.copy(get_resource_path("internal_versions"), version_file)
    return version_file


def _load_config():
    init_config(get_language_code(default_lang()), get_language_code(default_lang()))
    config_path = get_resource_path("CONFIG")
    with open(config_path, "r", encoding="utf-8") as config_f:
        config = json.load(config_f)
    return config


def _write_config(config):
    init_config(get_language_code(default_lang()), get_language_code(default_lang()))
    config_path = get_resource_path("CONFIG")
    with open(config_path, "w", encoding="utf-8") as config_f:
        json.dump(config, config_f)


def reset_config(app_lang: str = None, skill_lang: str = None):
    config_path = get_resource_path("CONFIG")
    if os.path.exists(config_path):
        os.remove(config_path)

    app_lang = app_lang.strip() if app_lang else default_lang()
    skill_lang = skill_lang.strip() if skill_lang else default_lang()

    if app_lang not in _language_code_mappings:
        app_lang = default_lang()

    if skill_lang not in _language_code_mappings:
        skill_lang = default_lang()

    init_config(get_language_code(app_lang), get_language_code(skill_lang))


def init_config(app_language_code, skill_language_code):
    config_path = get_resource_path("CONFIG")
    if not os.path.exists(config_path) or os.stat(config_path).st_size == 0:
        with open(config_path, "w", encoding="utf-8") as config_f:
            json.dump(
                {
                    "app-language": app_language_code,
                    "game-language": skill_language_code,
                    "black-bar-threshold": 10,
                },
                config_f,
            )


def get_app_language():
    config = _load_config()
    return (
        config["app-language"]
        if "app-language" in config
        else get_language_code(default_lang())
    )


def save_app_language(app_language_code):
    config = _load_config()
    config["app-language"] = app_language_code
    _write_config(config)


def translate_lang(lang):
    return _translated_langs[lang]


def untranslate_lang(lang):
    return _reverse_translated[lang]


def get_game_language():
    config = _load_config()
    return (
        config["game-language"]
        if "game-language" in config
        else get_language_code(default_lang())
    )


def get_black_bar_threshold():
    config = _load_config()
    return config["black-bar-threshold"] if "black-bar-threshold" in config else 10


def save_game_language(app_language_code):
    config = _load_config()
    config["game-language"] = app_language_code
    _write_config(config)


def save_ignored_update(version: SimpleSemVer):
    config = _load_config()
    config["skipped-version"] = str(version) if version is not None else version
    _write_config(config)


def get_ignored_update() -> SimpleSemVer:
    config = _load_config()
    try:
        return (
            SimpleSemVer(config["skipped-version"])
            if "skipped-version" in config
            else None
        )
    except:
        save_ignored_update(None)
        return None


def get_tesseract_location():
    config = _load_config()
    if "tesseract-directory" in config:
        return config["tesseract-directory"]
    return None


def save_tesseract_location(location):
    config = _load_config()
    config["tesseract-directory"] = location
    _write_config(config)


def reverse(dict_):
    reversed = {}
    for key in dict_:
        reversed[dict_[key]] = key
    return reversed


def default_lang():
    return "English"


_local_root = os.getenv("LOCALAPPDATA") or HOME if WINDOWS else HOME
_local_dir_name = "utsushis-charm"
_local_dir_full = os.path.join(
    _local_root,
    _local_dir_name,
)

_resources = {
    # masks/processing
    "lv1": _alter_resource_path(os.path.join("images", "levels", "lv1.png")),
    "lv2": _alter_resource_path(os.path.join("images", "levels", "lv2.png")),
    "lv3": _alter_resource_path(os.path.join("images", "levels", "lv3.png")),
    "slot0": _alter_resource_path(os.path.join("images", "slots", "slot0.png")),
    "slot1": _alter_resource_path(os.path.join("images", "slots", "slot1.png")),
    "slot2": _alter_resource_path(os.path.join("images", "slots", "slot2.png")),
    "slot3": _alter_resource_path(os.path.join("images", "slots", "slot3.png")),
    "slot4": _alter_resource_path(os.path.join("images", "slots", "slot4.png")),
    "mask": _alter_resource_path(os.path.join("images", "mask.png")),
    "charm_only": _alter_resource_path(os.path.join("images", "charm_only.png")),
    "skill_mask": _alter_resource_path(os.path.join("images", "skill_mask.png")),
    # internals
    "internal_versions": _alter_resource_path(os.path.join("data", "versions.json")),
    "INTERNAL_TRANSLATIONS": _alter_resource_path(os.path.join("data", "translations")),
    "INTERNAL_SKILLS": _alter_resource_path(os.path.join("data", "skills")),
    "LICENCES": _alter_resource_path("LICENSES"),
    "ICON": _alter_resource_path(os.path.join("media", "icon.ico")),
    # locals
    "versions": os.path.join(_local_dir_full, "versions.json"),
    "LOCAL_DIR": _local_dir_full,
    "LOCAL_TRANSLATIONS": os.path.join(_local_dir_full, "translations"),
    "LOCAL_SKILLS": os.path.join(_local_dir_full, "skills"),
    "CONFIG": os.path.join(_local_dir_full, "config.json"),
    # config_keys
    "app-language": "",
    "game-language": "game-language",
}


_language_code_mappings = {
    "English": "eng",
    "Japanese": "jpn",
    "French": "fra",
    "Italian": "ita",
    "German": "deu",
    "Spanish": "spa",
    "Russian": "rus",
    "Polish": "pol",
    "Korean": "kor",
    "Traditional Chinese": "chi_tra",
    "Simplified Chinese": "chi_sim",
}

_language_list = [
    "English",
    "Japanese",
    "French",
    "Italian",
    "German",
    "Spanish",
    "Russian",
    "Polish",
    "Korean",
    "Traditional Chinese",
    "Simplified Chinese",
]

# Most of these are probably wrong, I don't care.
_translated_langs = {
    "English": "English",
    "Japanese": "日本語",
    "French": "Français",
    "Italian": "Italiana",
    "German": "Deutsch",
    "Spanish": "Español",
    "Russian": "Русский",
    "Polish": "Polski",
    "Korean": "한국어",
    "Traditional Chinese": "繁體中文",
    "Simplified Chinese": "简体中文",
}

_reverse_translated = reverse(_translated_langs)
_reverse_language_code_mappings = reverse(_language_code_mappings)
