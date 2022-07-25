import os
import sys
import tkinter as tk

from .updater.Updater import Updater
from .frame_extraction import extract_unique_frames
from .charm_extraction import (
    extract_charms,
    save_charms,
    repair_invalid,
    remove_duplicates,
)
from .charm_encoding import encode_charms
from .arg_builder import build_args
from .utils import print_licenses
from .ui.AskUpdate import AskUpdate, UpdateType
from .ui.MainWindow import MainWindow
from .translator import Translator
from .resources import (
    default_lang,
    get_language_code,
    get_resource_path,
    get_app_language,
    reset_config,
    save_app_language,
    get_game_language,
    save_game_language,
    save_tesseract_location,
)
from .updater.updater_utils import (
    ask_main_update,
    ask_skill_update,
    ask_corrections_update,
)
from .updater.VersionChecker import VersionChecker

import logging
import json

logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level="INFO",
    force=True,
)

logger = logging.getLogger(__name__)


def handle_exception(exception, value, traceback):
    logger.error(f"An error occured {exception}, {value}, {str(traceback)}")
    logger.exception(f"An error occured")
    print("An error occured", exception, str(traceback))


def init_dirs():
    dirs_to_init = [
        get_resource_path("LOCAL_DIR"),
        get_resource_path("LOCAL_TRANSLATIONS"),
        get_resource_path("LOCAL_SKILLS"),
    ]
    for dir_to_init in dirs_to_init:
        os.makedirs(dir_to_init, exist_ok=True)


def read_default_args(args):
    if args.tess_dir is not None:
        save_tesseract_location(args.tess_dir)

    if args.app_language is not None:
        app_language_code = get_language_code(args.app_language)
        save_app_language(app_language_code)

    if args.language is not None:
        skill_language_code = get_language_code(args.language)
        save_game_language(skill_language_code)


def main(args):
    init_dirs()
    if args.license:
        print_licenses()
        sys.exit(0)

    if args.reset_config:
        reset_config(args.app_language, args.language)

    read_default_args(args)

    app_language_code = get_app_language()
    skill_language_code = get_game_language()

    if args.console:
        run_in_console(args)

    else:
        version_checker = VersionChecker()

        language_versions = version_checker.get_language_versions()

        for language_version in language_versions:
            lang, code, local, remote = language_version
            if local < remote:
                try:
                    Updater(
                        Translator(app_language_code), version_checker
                    ).update_language(code, remote)
                except Exception as e:
                    logger.error(
                        f"Error downloading language update for {lang} with error {e}"
                    )
                    pass

        main_window, translator = create_main_window(
            args,
            skill_language_code,
            app_language_code,
            list(map(lambda x: x[0], language_versions)),
        )

        new_app_update = ask_main_update(version_checker, main_window, translator)
        new_skills_update = ask_skill_update(version_checker, main_window, translator)

        new_corrections_update = ask_corrections_update(
            version_checker, main_window, skill_language_code, translator
        )

        main_window.mainloop()


def create_main_window(args, skill_language_code, app_language_code, app_langs):
    translator = Translator(app_language_code)
    new_window = MainWindow(translator, args, skill_language_code, app_langs)
    new_window.report_callback_exception = handle_exception
    sys.stdout = new_window

    return new_window, translator


def run_in_console(args):
    translator = Translator()
    input_dir = args.input_dir
    frame_dir = args.frame_dir
    charm_json = args.charm_json
    charm_encoded = args.charm_encoded

    lang = get_game_language()

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(frame_dir, exist_ok=True)

    if not args.skip_frames:
        extract_unique_frames(input_dir, frame_dir, translator)

    if not args.skip_charms:
        charms = extract_charms(frame_dir, lang, translator)
        if charms.has_invalids():
            charms = repair_invalid(lang, charms, translator)
            charms = remove_duplicates(charms, mode="a")

        save_charms(charms, charm_json)
        print(f"Saved {len(charms)} charms")

    print("Encoding charms")
    encode_charms(charm_json, charm_encoded)
    print(
        'Charms encoded under "charms.encoded.txt". Use the contents of that file on the MHR Wiki armor set builder'
    )

    if not args.autoexit:
        input("Press Enter to Exit...")
