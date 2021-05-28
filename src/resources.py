import os


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


_resources = {
    "skill_directory": _alter_resource_path(os.path.join("data", "skills")),
    "skill_corrections": "skill_corrections.csv",
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
