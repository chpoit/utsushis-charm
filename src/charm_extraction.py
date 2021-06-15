# 547,26 - 628,51
# 27*26

# Skill name size 216*21 # it appears those dimensions cause some slight shifting
# Skill 1: 413, 94
# Skill 2: 413, 144
# Skill 3: 413, 194 -> Jewels were not removed

# Level Size: 12 * 21
# Level 1: 618, 117
# Level 2: 618, 167
# Level 3: 618, 217 -> Jewels were not removed

from .parse_errors import ParseError
from .charm.Charm import Charm, CharmList, InvalidCharm
from .utils import *
from .resources import (
    get_resource_path,
    get_all_skills,
    load_corrections,
    get_spell_checker,
    add_corrections,
)
from .tesseract.Tesseract import Tesseract
from tqdm import tqdm
import numpy as np
import logging
import json
import cv2
import os

DEBUG = False


logger = logging.getLogger(__name__)
if DEBUG:
    logger.setLevel(logging.DEBUG)


def ask_repair(
    language,
    all_skills,
    spell,
    known_corrections,
    skill_img,
    parsed_text,
    level,
    _: lambda x: x,
):
    has_errored = False
    reconstructed_skill = ""
    while True:
        for w in parsed_text.split():
            if w in known_corrections:
                true_w = known_corrections[w]
                reconstructed_skill += true_w + " "
                continue

            suggestions = spell.lookup(w, 2)
            print(f"\nParsed Text: '{parsed_text}' Level {level}")
            print(f"Current word: '{w}'")
            if len(suggestions) == 0:
                print("Too many errors in the word, no suggestions")
            if len(suggestions) > 1:
                print("Corrections: ")
                for i, s in enumerate(suggestions):
                    print(f"[{i}] {s.term}")
            cv2.imshow(f"{parsed_text}", skill_img)
            cv2.waitKey(1)

            while True:
                if len(suggestions) == 1 and not has_errored:
                    new_word = ""
                else:
                    new_word = input(
                        f"Select Correction for word '{w}', or type it in. [0] is default. Type 'empty' for no skill, Type 'cancel' to skip this charm:"
                    )
                has_errored = False

                if new_word == "empty":
                    return "<EMPTY>"
                elif new_word == "cancel":
                    return "<CANCELLED>"
                if str.isdigit(new_word) or not new_word:
                    if not new_word:
                        new_word = 0
                    idx = int(new_word)
                    if idx >= len(suggestions):
                        continue
                    reconstructed_skill += suggestions[idx].term + " "
                else:
                    reconstructed_skill += new_word + " "
                break

            cv2.destroyWindow(f"{parsed_text}")

        reconstructed_skill = reconstructed_skill.strip()
        if not is_skill(all_skills, reconstructed_skill):
            if len(suggestions) == 1:
                reconstructed_skill = ""
                has_errored = True
                continue
            print(f"'{reconstructed_skill}' is not a valid skill.")
            print(
                "Make sure you only correct one word at a time. You can look at the picture to help identify the proper skill."
            )
            reconstructed_skill = ""
        else:
            logger.info(f"Corrected skill: {reconstructed_skill} from {parsed_text}")
            new_corrections = [
                (w, r) for w, r in zip(parsed_text.split(), reconstructed_skill.split())
            ]

            add_corrections(language, known_corrections, *new_corrections)
            break

    skill = reconstructed_skill.strip()
    return skill


def repair_invalid(language, charms, _=lambda x: x, repair_callback=ask_repair):
    spell_checker = get_spell_checker(language)
    known_corrections = load_corrections(language)
    all_skills = get_all_skills(language)

    fixed = []
    for charm in charms:
        if type(charm) == InvalidCharm:
            cancel = False
            fixed_skills = charm.skills
            errors = charm.get_errors()
            for img, parsed_text, level, error in errors:
                repaired = repair_callback(
                    language,
                    all_skills,
                    spell_checker,
                    known_corrections,
                    img,
                    parsed_text,
                    level,
                    _,
                )
                if repaired == "<EMPTY>":
                    continue
                elif repaired == "<CANCELLED>":
                    logger.warning(
                        f"Charm skipped and removed through cancellation: {charm.frame_loc}"
                    )
                    cancel = True
                    break

                fixed_skills[repaired] = level
            if not cancel:
                fixed.append(charm.repair(fixed_skills))
        else:
            fixed.append(charm)

    return fixed


def extract_charm(frame_loc, slots, skills, skill_text, all_skills, known_corrections):
    logger.debug(f"Starting charm for {frame_loc}")
    suggestions = []
    has_errored = False
    skill_number = 0
    charm = Charm(slots, frame_loc=frame_loc)
    errors = []
    for (img, text) in zip(skills, skill_text):
        skill_number += 1
        skill_img, _ = img
        skill, level = text
        skill = skill.strip()

        if not skill:
            logger.warning(
                f"Empty skill string for skill {skill_number} on {frame_loc}"
            )
            errors.append((skill_img, skill, level, ParseError.NO_SKILL))
            continue

        if not is_skill(all_skills, skill):
            reconstructed_skill = ""
            for w in skill.split():
                if w in known_corrections:
                    true_w = known_corrections[w]
                    reconstructed_skill += f"{true_w} "
                else:
                    break
            skill = reconstructed_skill

        if is_skill(all_skills, skill):
            skill = fix_skill_name(all_skills, skill)
            charm.add_skill(skill, level)
            logger.debug(f"Parsed and added skill: {skill.strip()}, level: {level}")
        else:
            errors.append((skill_img, text[0], level, ParseError.MUST_FIX))
            logger.debug(f"Failed to parse skill {text[0].strip()}, level: {level}")

    if len(errors) > 0:
        logger.warning(f"Charm for {frame_loc} has errors")
        charm = InvalidCharm(charm, errors)
    else:
        logger.debug(f"Finished charm for {frame_loc}")

    logger.debug(f"{frame_loc}: {charm.to_dict()}")
    return charm


def extract_charms(
    frame_dir,
    language="eng",
    _=lambda x: x,
    iter_wrapper=None,
    charm_callback=lambda x: None,
):
    known_corrections = load_corrections(language)
    all_skills = get_all_skills(language)

    if not iter_wrapper:
        iter_wrapper = tqdm
    tess = Tesseract(language=language, _=_)
    charms = []

    try:
        frames = list(map(lambda frame_loc: frame_loc.path, os.scandir(frame_dir)))

        def keep_existing_and_update(x):
            i, x = x
            if x:

                return x

        with iter_wrapper(frames, desc=_("parsing-skills-slots")) as parse_pbar:
            count = 0
            combined_data = []
            for frame_loc in parse_pbar:
                charm_tuple = extract_basic_info(tess, frame_loc, cv2.imread(frame_loc))
                if charm_tuple:
                    count += 1
                    charm_callback({"charm_count": count})
                    combined_data.append(charm_tuple)

        with iter_wrapper(combined_data, desc=_("validate-fix")) as build_pbar:
            for frame_loc, slots, skills, skill_text in build_pbar:
                try:
                    charm = extract_charm(
                        frame_loc,
                        slots,
                        skills,
                        skill_text,
                        all_skills,
                        known_corrections,
                    )
                    if charm.has_skills():
                        charms.append(charm)
                    else:
                        logger.warn(_("logger-skill-less").format(frame_loc))
                except Exception as e:
                    logger.error(_("logger-charm-error").format(frame_loc, e))
                    logger.exception("Traceback")

    except Exception as e:
        logger.error(f"Crashed with {e}")
        logger.exception("Traceback")

    return remove_duplicates(charms, charm_callback)


def remove_duplicates(charms, charm_callback=lambda x: None, mode="w"):
    unique_charms = CharmList(charms)
    charm_callback({"unique_charms": len(unique_charms)})
    if len(charms) != len(unique_charms):
        print("Pre-duplicate", len(charms))
        print("Post-duplicate:", len(unique_charms))
        save_duplicates(charms)

    return unique_charms


def save_duplicates(charms, mode="w"):
    dupe_file_name = "charm.duplicates.txt"
    charm_dupes = {}
    for charm in charms:
        frame_loc = charm.frame_loc
        if charm not in charm_dupes:
            charm_dupes[charm] = []
        charm_dupes[charm].append(frame_loc)

    with open(dupe_file_name, mode) as dupe_file:
        for charm in filter(lambda x: len(charm_dupes[x]) > 1, charm_dupes):
            locations = charm_dupes[charm]
            dupe_file.write(f"{charm.to_dict()}\n")
            for frame_loc in locations:
                dupe_file.write(f"{frame_loc}\n")
            dupe_file.write("\n")

    print(f"Duplicate charms can be found in {dupe_file_name}")


def extract_basic_info(tess: Tesseract, frame_loc, frame):
    try:
        skill_only_im = remove_non_skill_info(frame)
        slots = get_slots(skill_only_im)

        inverted = cv2.bitwise_not(skill_only_im)

        trunc_tr = apply_trunc_threshold(inverted)  # appears to work best

        skills = get_skills(trunc_tr, True)

        skill_text = read_text_from_skill_tuple(tess, skills)
        return frame_loc, slots, skills, skill_text
    except Exception as e:
        logger.error(f"An error occured when analysing frame {frame_loc}. Error: {e}")
        logger.exception("Traceback")
        return None


def save_charms(charms: CharmList, charm_json):
    with open(charm_json, "w", encoding="utf-8") as charm_file:
        json.dump(charms.to_dict(), charm_file)


if __name__ == "__main__":
    frame_dir = "frames"
    charm_json = "charms.json"

    charms = extract_charms(frame_dir)

    save_charms(charms, charm_json)
