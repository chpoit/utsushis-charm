import os
import shutil
import json
from urllib import request
import logging

from ..resources import (
    get_lastest_api_url,
    get_resource_path,
    get_update_url,
    get_versions_location,
    get_language_list,
    get_language_code,
    get_language_from_code,
)
from .SimpleSemVer import SimpleSemVer

logger = logging.getLogger(__name__)


class VersionChecker:
    def __init__(self):
        self.snapshot = None
        self.latest_description = None
        self.snapshot = self._get_online_versions()
        self.latest_description = str(self._get_latest_body()).replace("\r", "")

    def check_app_version(self):
        local = self._get_version(True, "app")
        remote = self._get_version(False, "app")
        return self.is_outdated(local, remote), local, remote

    def check_skill_version(self):
        local = self._get_version(True, "skills")
        remote = self._get_version(False, "skills")
        return self.is_outdated(local, remote), local, remote

    def check_language_version(self, lang):
        local = self._get_version(True, "languages", lang)
        remote = self._get_version(False, "languages", lang)
        return self.is_outdated(local, remote), local, remote

    def check_correction_version(self, lang):
        local = self._get_version(True, "corrections", lang)
        remote = self._get_version(False, "corrections", lang)
        return self.is_outdated(local, remote), local, remote

    def update_local_language_version(self, lang, version: SimpleSemVer):
        self._write_new_version(version, "languages", lang)

    def update_skill_version(self, version: SimpleSemVer):
        self._write_new_version(version, "skills")

    def update_corrections_version(self, lang, version: SimpleSemVer):
        self._write_new_version(version, "corrections", lang)

    def is_outdated(self, local, remote):
        return local < remote

    def get_latest_description(self):
        return self.latest_description

    def get_language_versions(self):
        versions = []
        language_list = get_language_list()
        codes = list(map(get_language_code, language_list))
        for code in codes:
            local = self._get_version(True, "languages", code)
            remote = self._get_version(False, "languages", code)
            if local == 0 and remote == 0:
                continue
            else:
                versions.append((code, local, remote))

        return list(
            map(lambda x: (get_language_from_code(x[0]), x[0], x[1], x[2]), versions)
        )

    def _ensure_proper_app_version(self):
        with open(get_resource_path("internal_versions"), encoding="utf-8") as internal:
            internal_data = json.load(internal)
        internal_version = internal_data["app"]
        self._write_new_version(internal_version, "app")

    def _write_new_version(self, version: SimpleSemVer, main_key, sub_key=None):
        version = str(version)
        with open(get_resource_path("versions"), encoding="utf-8") as local:
            local_data = json.load(local)

        if sub_key is not None:
            local_data[main_key][sub_key] = version
        else:
            local_data[main_key] = version

        with open(get_resource_path("versions"), "w", encoding="utf-8") as local:
            json.dump(local_data, local)

    def _get_version(self, local: bool, main_key, sub_key=None):
        if local:
            versions = self._load_local_versions()
        else:
            versions = self._get_online_versions()

        return self._get_version_number(versions, main_key, sub_key)

    def _get_version_number(self, versions, main_key, sub_key=None):
        if versions is None:
            return SimpleSemVer()
        version = versions[main_key]
        if sub_key is not None:
            version = version[sub_key]
        return SimpleSemVer(version)

    def _load_local_versions(self):
        version_path = get_versions_location()

        self._ensure_proper_app_version()

        with open(version_path, encoding="utf-8") as version_file:
            versions = json.load(version_file)

        return versions

    def _get_online_versions(self):
        if self.snapshot is not None:
            return self.snapshot

        url = get_update_url()
        try:
            online_versions = request.urlopen(url).read().decode()
            return json.loads(online_versions)
        except request.HTTPError as e:
            sc = e.code
            logger.exception(f"Could not load online versions: {sc}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred loading online versions")
            return None

    def _get_latest_body(self):
        if self.latest_description is not None:
            return self.latest_description
        # curl -H "Accept: application/vnd.github+json"
        url = get_lastest_api_url()
        try:
            data_string = request.urlopen(url).read().decode()
            data = json.loads(data_string)
            if "body" in data:
                return data["body"]
            return None
        except request.HTTPError as e:
            sc = e.code
            logger.exception(f"Could not load update description: {sc}")
            return None
        except Exception as e:
            logger.exception(
                f"An unexpected error occurred loading update information: {sc}"
            )
            return None
