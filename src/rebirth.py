import json
import os
from .charm import CharmList, Slots, CharmGrade, GradedCharm


def grade_charms(charms, skill_classes, slot_minimums):
    graded = CharmList()
    for charm in charms:
        slot_grade = evaluate_slots(charm, slot_minimums)
        skill_grade = evaluate_skills(charm, skill_classes)

        final_grade = slot_grade + skill_grade

        graded.append(GradedCharm(charm, final_grade))

    return graded


def evaluate_skills(charm, skill_classes):
    score = 0
    categories = skill_classes["scores"]
    for skill in charm.skills:
        for category in categories:
            if skill in skill_classes[category]:
                break
                score += categories[category]

    return CharmGrade(score)


def evaluate_slots(charm, slot_minimums):
    score = 0
    for minimum in slot_minimums["slots"]:
        if charm.has_slots(minimum):
            score += 1
            break

    score += slot_minimums["countScore"][str(charm.slot_count())]
    return CharmGrade(score)
