from ..resources import get_ignored_update, save_ignored_update
from .VersionChecker import VersionChecker
from .Updater import Updater
from ..ui.AskUpdate import UpdateAction, AskUpdate, UpdateType


def ask_main_update(version_checker: VersionChecker, main_window, _):
    new_update, cur_ver, online_ver = version_checker.check_app_version()

    answer = UpdateAction.Nothing
    if new_update:
        skipped = get_ignored_update()
        if skipped is not None and online_ver == skipped:
            return answer

        answer = _spawn_window(
            main_window, _, UpdateType.App, cur_ver, online_ver, True
        )
        if answer == UpdateAction.Update:
            updater = Updater(_, version_checker)
            updater.update_main_app()

        elif answer == UpdateAction.Ignore:
            save_ignored_update(online_ver)

    return answer


def ask_skill_update(version_checker: VersionChecker, main_window, _):
    new_update, cur_ver, online_ver = version_checker.check_skill_version()

    answer = UpdateAction.Nothing
    if new_update:
        answer = _spawn_window(main_window, _, UpdateType.Skills, cur_ver, online_ver)
        if answer == UpdateAction.Update:
            updater = Updater(_, version_checker)
            updater.update_all_skills(online_ver)
    return answer


def ask_corrections_update(
    version_checker: VersionChecker, main_window, skill_language_code, _
):
    new_update, cur_ver, online_ver = version_checker.check_correction_version(
        skill_language_code
    )

    answer = UpdateAction.Nothing
    if new_update:
        answer = _spawn_window(
            main_window, _, UpdateType.SkillCorrections, cur_ver, online_ver
        )
        if answer == UpdateAction.Update:
            updater = Updater(_, version_checker)
            updater.update_skill_corrections(skill_language_code, online_ver)
    return answer


def _spawn_window(main_window, _, update_type, cur_ver, online_ver, show_ignore=False):
    askup = AskUpdate(main_window, _, update_type, cur_ver, online_ver, show_ignore)
    main_window.wait_window(askup)
    return askup.answer
