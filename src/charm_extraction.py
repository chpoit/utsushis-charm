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

from .Charm import Charm
from .utils import *
from tqdm import tqdm
from symspellpy.symspellpy import SymSpell
import numpy as np
import logging
import json
import cv2
import os
from joblib import Parallel, delayed
DEBUG = False


logger = logging.getLogger(__name__)
if DEBUG:
    logger.setLevel(logging.DEBUG)


spell = SymSpell(max_dictionary_edit_distance=4)
spell.load_dictionary(get_resource_path("skill_dict"), 0, 1)


known_corrections = {}
with open(get_resource_path('skill_corrections'), encoding='utf-8') as scf:
    for line in scf.readlines():
        line = line.strip()
        w, r = line.split(',')
        known_corrections[w] = r


all_skills = {}
with open(get_resource_path('skill_list')) as slf:
    for line in slf.readlines():
        skill_name = line.strip()
        all_skills[skill_name.lower()] = skill_name


def is_skill(skill_dict, skill_name):
    return skill_name.lower().strip() in skill_dict


def fix_skill_name(skill_dict, skill_name):
    return skill_dict[skill_name.lower()]


def extract_charm(frame_loc, slots, skills, skill_text):
    logger.debug(f"Starting charm for {frame_loc}")
    has_errored = False
    charm = Charm(slots)
    skill_number = 0
    for (img, text) in zip(skills, skill_text):
        skill_number += 1
        skill_img, _ = img
        skill, level = text
        skill = skill.strip()

        if not skill:
            logger.warning(
                f"Empty skill string for skill {skill_number} on {frame_loc}")
            continue

        if is_skill(all_skills, skill):
            logger.debug(f"Added {skill}, {level}")
            charm.add_skill(skill, level)
            continue

        logger.info("Parsed skill: ", skill.strip(), "level", level)

        reconstructed_skill = ""
        while (True):
            for w in skill.split():
                if w in known_corrections:
                    true_w = known_corrections[w]
                    reconstructed_skill += true_w + " "
                    if reconstructed_skill.strip() == "<EMPTY_SKILL>":
                        break
                    continue

                suggestions = spell.lookup(w, 2)
                print(f"\nFull skill: '{skill}' Level {level}")
                print(f"Current word: '{w}'")
                if len(suggestions) == 0:
                    print("Too many errors in the word")
                if len(suggestions) > 1:
                    print("Corrections: ")
                    for i, s in enumerate(suggestions):
                        print(f"[{i}] {s.term}")
                cv2.imshow(f"{skill}", skill_img)
                cv2.waitKey(1)

                while (True):
                    if len(suggestions) == 1 and not has_errored:
                        new_word = ""
                    else:
                        new_word = input(
                            f"Select Correction for word '{w}', or type it in. [0] is default. Type 'empty' for no skill:")
                    has_errored = False

                    if new_word == "empty":
                        reconstructed_skill = "<EMPTY_SKILL>"
                        break
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

                cv2.destroyWindow(f"{skill}")

            reconstructed_skill = reconstructed_skill.strip()
            if "<EMPTY_SKILL>" in reconstructed_skill:
                with open(get_resource_path("skill_corrections"), "a") as scf:
                    scf.write(f"{w.strip()},{reconstructed_skill}\n")
                known_corrections[skill] = reconstructed_skill
            elif not is_skill(all_skills, reconstructed_skill):
                if len(suggestions) == 1:
                    reconstructed_skill = ""
                    has_errored = True
                    continue
                print(f"'{reconstructed_skill}' is not a valid skill.")
                print(
                    "Make sure you only correct one word at a time. You can look at the picture to help identify the proper skill.")
                reconstructed_skill = ""
            else:
                logger.info(
                    f"Corrected skill: {reconstructed_skill} from {skill}")
                for w, r in zip(skill.split(), reconstructed_skill.split()):
                    if w not in known_corrections:
                        with open(get_resource_path("skill_corrections"), "a", encoding="utf-8") as scf:
                            scf.write(f"{w.strip()},{r.strip()}\n")
                        known_corrections[w] = r
                break

        skill = reconstructed_skill.strip()
        if "<EMPTY_SKILL>" in skill:
            logger.warning(f"Empty/invalid skill found on {frame_loc}")
            continue

        logger.debug(f"Added {skill}, {level}")
        charm.add_skill(fix_skill_name(all_skills, skill), level)

    logger.debug(f"Finished charm for {frame_loc}")
    logger.debug(f"{frame_loc}: {charm.to_dict()}")

    return charm


def extract_charms(frame_dir, max_cpu=os.cpu_count()-1):
    charms = []
    charm_loc = []
    jobs = max(1, max_cpu)
    print(f"Using {jobs} thread(s)")
    try:
        frames = list(
            map(lambda frame_loc: (frame_loc.path, cv2.imread(
                frame_loc.path)), os.scandir(frame_dir))
        )

        with tqdm(frames, desc="Parsing skill and slots") as tqdm_iter:
            combined_data = Parallel(n_jobs=jobs)(
                delayed(extract_basic_info)(frame_loc, frame) for frame_loc, frame in tqdm_iter)
            combined_data = list(filter(lambda x: x, combined_data))

        for frame_loc, slots, skills, skill_text in tqdm(combined_data, desc="Validating and fixing charms"):
            try:
                charm = extract_charm(frame_loc, slots, skills, skill_text)
                if charm.has_skills():
                    charms.append(charm)
                    charm_loc.append(frame_loc)
                else:
                    logger.warn(f"Skill-less charm found in {frame_loc}")
            except Exception as e:
                logger.error(
                    f"An error occured when extracting charm on {frame_loc}. Error: {e}")

    except Exception as e:
        logger.error(f"Crashed with {e}")

    unique_charms = set(charms)
    if len(charms) != len(unique_charms):
        print("Pre-duplicate", len(charms))
        print("Post-duplicate:", len(unique_charms))
        save_duplicates(charm_loc, charms)

    return unique_charms


def save_duplicates(charm_loc, charms):
    dupe_file_name = "charm.duplicates.txt"
    charm_dupes = {}
    for frame_loc, charm in zip(charm_loc, charms):
        if charm not in charm_dupes:
            charm_dupes[charm] = []
        charm_dupes[charm].append(frame_loc)

    with open(dupe_file_name, "w") as dupe_file:
        for charm in filter(lambda x: len(charm_dupes[x]) > 1, charm_dupes):
            locations = charm_dupes[charm]
            dupe_file.write(f"{charm.to_dict()}\n")
            for frame_loc in locations:
                dupe_file.write(f"{frame_loc}\n")
            dupe_file.write("\n")

    print(f"Duplicate charms can be found in {dupe_file_name}")


def extract_basic_info(frame_loc, frame):
    try:
        skill_only_im = remove_non_skill_info(frame)
        slots = get_slots(skill_only_im)

        inverted = cv2.bitwise_not(skill_only_im)

        trunc_tr = apply_trunc_threshold(inverted)  # appears to work best

        skills = get_skills(trunc_tr, True)

        skill_text = read_text_from_skill_tuple(skills)
        return frame_loc, slots, skills, skill_text
    except Exception as e:
        logger.error(
            f"An error occured when analysing frame {frame_loc}. Error: {e}")
        return None


def save_charms(charms, charm_json):
    with open(charm_json, "w") as charm_file:
        charms = list(map(lambda x: x.to_dict(), charms))
        json.dump(charms, charm_file)


if __name__ == "__main__":
    frame_dir = "frames"
    charm_json = "charms.json"

    charms = extract_charms(frame_dir)

    save_charms(charms, charm_json)
