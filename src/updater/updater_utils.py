from .VersionChecker import VersionChecker
from .Updater import Updater
from ..ui.AskUpdate import AskUpdate, UpdateType


def ask_main_update(main_window, _):
    version_checker = VersionChecker()
    updater = Updater(_, version_checker)
    new_update, cur_ver, online_ver = version_checker.check_app_version()

    answer = False
    if new_update:
        answer = _spawn_window(main_window, _, UpdateType.App, cur_ver, online_ver)
        if answer:
            updater.update_main_app()
    return answer


def ask_language_update(main_window, app_language_code, _):
    version_checker = VersionChecker()
    updater = Updater(_, version_checker)
    new_update, cur_ver, online_ver = version_checker.check_language_version(
        app_language_code
    )

    answer = False
    if new_update:
        answer = _spawn_window(
            main_window, _, UpdateType.AppLanguage, cur_ver, online_ver
        )
        if answer:
            updater.update_language(app_language_code, online_ver)
    return answer


def _spawn_window(main_window, _, update_type, cur_ver, online_ver):
    askup = AskUpdate(main_window, _, update_type, cur_ver, online_ver)
    main_window.wait_window(askup)
    return askup.answer
