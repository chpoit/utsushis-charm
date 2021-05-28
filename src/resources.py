import os
import shutil
import platform
from pathlib import Path
from symspellpy.symspellpy import SymSpell


HOME = str(Path.home())
WINDOWS = platform.system() == "Windows"


def get_all_skills(lang="eng"):
    all_skills = {}
    skill_dir = get_resource_path("skill_directory")
    skill_file = os.path.join(skill_dir, f"skills.{lang}.txt")
    with open(skill_file, encoding="utf-8") as slf:
        for line in slf.readlines():
            skill_name = line.strip()
            all_skills[skill_name.lower()] = skill_name
    return all_skills


def get_word_freqs_location(lang="eng"):
    skill_dir = get_resource_path("skill_directory")
    return os.path.join(skill_dir, f"skills.{lang}.freq")


def get_resource_path(resource):
    return _resources[resource] if resource in _resources else resource


def _alter_resource_path(relative_path):
    import sys

    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_language_list():
    return _language_list


def get_language_code(language):
    return _language_code_mappings[language]


def get_language_from_code(language_code):
    return _reverse_language_code_mappings[language_code]


def load_corrections(language_code, known_corrections=None):
    known_corrections = known_corrections or {}
    corrections_path = _corrections_path(language_code)
    if not os.path.exists(corrections_path):
        _create_default_skill_corrections(language_code)

    with open(corrections_path, encoding="utf-8") as scf:
        known_corrections = {
            w: c for w, c in map(lambda x: x.strip().split(","), scf.readlines())
        }

    return known_corrections


def get_spell_checker(language_code):
    spell = SymSpell(max_dictionary_edit_distance=4)
    spell.load_dictionary(get_word_freqs_location(language_code), 0, 1)
    return spell


def add_corrections(language_code, known_corrections, *new_tuples):
    corrections_path = _corrections_path(language_code)
    with open(corrections_path, "a", encoding="utf-8") as c_fp:
        for a, b in new_tuples:
            if not a in known_corrections:
                known_corrections[a] = b
                c_fp.write(f"{a},{b}\n")
    return known_corrections


def _create_default_skill_corrections(language_code):
    packaged_corrections = _alter_resource_path(
        os.path.join("data", "skills", f"corrections.{language_code}.csv")
    )
    corrections_path = _corrections_path(language_code)
    shutil.copy(packaged_corrections, corrections_path)


def _corrections_path(language_code):
    return get_resource_path("skill_corrections").format(language_code)


_resources = {
    "skill_directory": _alter_resource_path(os.path.join("data", "skills")),
    "skill_corrections": os.path.join(
        (os.getenv("LOCALAPPDATA") or HOME if WINDOWS else HOME),
        "utsushis-charm",
        "corrections.{}.csv",
    ),
    "lv1": _alter_resource_path(os.path.join("images", "levels", "lv1.png")),
    "lv2": _alter_resource_path(os.path.join("images", "levels", "lv2.png")),
    "lv3": _alter_resource_path(os.path.join("images", "levels", "lv3.png")),
    "slot0": _alter_resource_path(os.path.join("images", "slots", "slot0.png")),
    "slot1": _alter_resource_path(os.path.join("images", "slots", "slot1.png")),
    "slot2": _alter_resource_path(os.path.join("images", "slots", "slot2.png")),
    "slot3": _alter_resource_path(os.path.join("images", "slots", "slot3.png")),
    "mask": _alter_resource_path(os.path.join("images", "mask.png")),
    "charm_only": _alter_resource_path(os.path.join("images", "charm_only.png")),
    "skill_mask": _alter_resource_path(os.path.join("images", "skill_mask.png")),
    "licences": _alter_resource_path("LICENSES"),
    "TRANSLATIONS": _alter_resource_path(os.path.join("data", "translation")),
    "ICON": _alter_resource_path(os.path.join("media", "icon.ico")),
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

_reverse_language_code_mappings = {
    "eng": "English",
    "jpn": "Japanese",
    "fra": "French",
    "ita": "Italian",
    "deu": "German",
    "spa": "Spanish",
    "rus": "Russian",
    "pol": "Polish",
    "kor": "Korean",
    "chi_tra": "Traditional Chinese",
    "chi_sim": "Simplified Chinese",
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
