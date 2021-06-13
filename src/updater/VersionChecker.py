import os
import shutil
import json
from urllib import request
import logging

from ..resources import get_resource_path
from .SimpleSemVer import SimpleSemVer

logger = logging.getLogger(__name__)


class VersionChecker:
    def check_app_version(self):
        local = _get_version(True, "app")
        remote = _get_version(False, "app")
        return is_outdated(local, remote), local, remote

    def check_skill_version(self):
        local = _get_version(True, "skills")
        remote = _get_version(False, "skills")
        return is_outdated(local, remote), local, remote

    def check_language_version(self, lang):
        local = _get_version(True, "languages", lang)
        remote = _get_version(False, "languages", lang)
        return is_outdated(local, remote), local, remote

    def check_correction_version(self, lang):
        local = _get_version(True, "corrections", lang)
        remote = _get_version(False, "corrections", lang)
        return is_outdated(local, remote), local, remote

    def is_outdated(self, local, remote):
        local = SimpleSemVer(local)
        remote = SimpleSemVer(remote)
        return local < remote

    def _load_local_versions(self):
        version_path = get_resource_path("versions")
        if not os.path.exists(version_path):
            self._create_local_versions()

        with open(version_path) as version_file:
            versions = json.load(version_file)

        return versions

    def _create_local_versions(self):
        shutil.copy(
            get_resource_path("internal_versions"), get_resource_path("versions")
        )

    def _get_version(self, local: bool, versions, main_key, sub_key=None):
        if local:
            versions = _load_local_versions()
        else:
            versions = _get_online_versions()

        return _get_version_number(versions, main_key, sub_key)

    def _get_version_number(self, versions, main_key, sub_key=None):
        if versions is None:
            return SimpleSemVer()
        version = versions[main_key]
        if sub_key is not None:
            version = version[sub_key]
        return SimpleSemVer(version)

    def _get_online_versions(self):
        url = "https://raw.githubusercontent.com/chpoit/utsushis-charm/master/data/versions.json"
        try:
            online_versions = request.urlopen(url).read().decode()
            return json.loads(online_versions)
        except request.HTTPError as e:
            sc = e.response.status_code
            logger.exception(f"Could not load online versions: {sc}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred loading online versions")
            return None
