import webbrowser
from ..resources import (
    get_latest_url,
    get_language_url,
    get_corrections_url,
    get_corrections_path,
    get_translation_location,
)
from .VersionChecker import VersionChecker
from urllib import request
from pathlib import Path
import logging
import shutil
from ..updater.SimpleSemVer import SimpleSemVer

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

    def update_skill_corrections(self, lang, new_version: SimpleSemVer):
        _ = self._
        url = get_corrections_url(lang)

        full_name = get_corrections_path(lang)
        full_name_new = f"{full_name}.new"
        try:
            Path(full_name_new).touch()
            request.urlretrieve(url, filename=full_name_new, data=None)
            self.version_checker.update_corrections_version(lang, new_version)
        except PermissionError as e:
            logger.exception("Could not write language file")
            print(_("skill-cor-permission-denied"))
            return

        self.merge_corrections(full_name, full_name_new)

    def update_all_skills(self):
        pass

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
