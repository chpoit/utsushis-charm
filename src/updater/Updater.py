import webbrowser
import json
import os
from ..resources import (
    get_latest_url,
    get_language_url,
    get_corrections_url,
    get_corrections_path,
    get_translation_location,
    get_english_skill_mapping_url,
    get_english_skill_mappping_location,
)
from .VersionChecker import VersionChecker
from urllib import request
from pathlib import Path
import logging
import shutil
from . import SimpleSemVer
from ..resources import get_resource_path

logger = logging.getLogger(__name__)


class Updater:
    def __init__(self, _, version_checker: VersionChecker = None):
        self.version_checker = version_checker
        self._ = _

    def update_main_app(self):
        webbrowser.open(get_latest_url())

    def update_language(self, lang, new_version: SimpleSemVer):
        _ = self._
        url = get_language_url(lang)

        full_name = get_translation_location(lang)
        try:
            Path(full_name).touch()
            request.urlretrieve(url, filename=full_name, data=None)
            self.version_checker.update_local_language_version(lang, new_version)
        except PermissionError as e:
            logger.exception("Could not write language file")
            print(_("lang-permission-denied"))
        except Exception as e:
            logger.exception("An error occurred")

    def update_skill_corrections(self, lang, new_version: SimpleSemVer):
        _ = self._
        url = get_corrections_url(lang)

        full_name = get_corrections_path(lang)
        full_name_new = f"{full_name}.new"
        try:
            Path(full_name_new).touch()
            request.urlretrieve(url, filename=full_name_new, data=None)
            self.version_checker.update_corrections_version(lang, new_version)
            self.merge_corrections(full_name, full_name_new)
        except PermissionError as e:
            logger.exception("Could not write corrections file")
            print(_("skill-cor-permission-denied"))
        except Exception as e:
            logger.exception("An error occurred")

    def update_all_skills(self, new_version: SimpleSemVer):
        url = get_english_skill_mapping_url()
        full_name = get_english_skill_mappping_location()
        try:
            Path(full_name).touch()
            request.urlretrieve(url, filename=full_name, data=None)
            self.rebuild_skills_from_file(full_name)
            self.version_checker.update_skill_version(new_version)
        except PermissionError as e:
            logger.exception("Could not write skill file")
            print(_("skill-permission-denied"))
        except Exception as e:
            logger.exception("An error occurred")

    def merge_corrections(self, full_name, full_name_new):
        with open(full_name, "r", encoding="utf-8") as old_f:
            old = set(old_f.readlines())
        with open(full_name_new, "r", encoding="utf-8") as new_f:
            new = set(new_f.readlines())

        with open(full_name_new, "w", encoding="utf-8") as new_f:
            for line in sorted(old.union(new)):
                new_f.write(line)
        try:
            shutil.move(full_name_new, full_name)
        except:
            logger.exception("Could not merge skill corrections")

    def rebuild_skills_from_file(self, en_skill_dict):
        with open(en_skill_dict, "r", encoding="utf-8") as skill_file:
            data = json.load(skill_file)

        reversed_skills = {lang_code: {} for lang_code in data}
        for lang_code in data:
            skill_dir = get_resource_path("LOCAL_SKILLS")
            skill_file_name = os.path.join(skill_dir, f"skills.{lang_code}.txt")
            freq_file_name = os.path.join(skill_dir, f"skills.{lang_code}.freq")

            freq_dict = {}
            with open(skill_file_name, "w", encoding="utf-8") as skill_file:
                for lang_skill in sorted(data[lang_code].values()):
                    skill_file.write(f"{lang_skill}\n")
                    skill_words = lang_skill.split()
                    for word in skill_words:
                        if not word in freq_dict:
                            freq_dict[word] = 0
                        freq_dict[word] += 1

            with open(freq_file_name, "w", encoding="utf-8") as freq_file:
                for word in sorted(freq_dict):
                    freq_file.write(f"{word} {freq_dict[word]}\n")

            for skill in data[lang_code]:
                reversed_skills[lang_code][data[lang_code][skill]] = skill

        with open(en_skill_dict.replace(".en.", ".alt."), "w", encoding="utf-8") as rev:
            json.dump(reversed_skills, rev, ensure_ascii=False)
