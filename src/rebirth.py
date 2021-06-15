# ranking base on god talisman checker at https://gamewith.net/monsterhunter-rise/article/show/28392

import json
import os

slotValue = [500, 3500, 4000]


# compare if a charm can be make with another
def isCharm1InCharm2(charm1, charm2, skillToJewel):
    charmToSlot = [0, 0, 0]

    for slot in charm1["slots"]:
        if slot > 0:
            charmToSlot[slot - 1] += 1

    for skill in charm1["skillsLst"]:
        skillDif = charm1["skills"][skill]

        if skill in charm2["skillsLst"]:
            skillDif = charm1["skills"][skill] - charm2["skills"][skill]

        if skillDif > 0 and not skill in skillToJewel:
            return False

        charmToSlot[skillToJewel[skill] - 1] += skillDif if skillDif > 0 else 0

    for slot in charm2["slots"]:
        if slot > 0 and sum(charmToSlot[:slot]) > 0:
            charmToSlot[slot - 1] -= 1

    return True if sum(charmToSlot) <= 0 else False


# give a rank and list of used skill for each charm
def charmsGrader(charms):
    for charm in charms:
        grade = 0

        skillsLst = list(charm["skills"].keys())
        charm["skillsLst"] = list(
            filter(lambda skill: skill not in trashSkills, skillsLst)
        )
        charm["skillsLst"].sort()

        for skill in charm["skillsLst"]:
            score = next(
                (
                    scoreSkill["score"]
                    for scoreSkill in scoreSkills
                    if scoreSkill["name"] == skill
                ),
                0,
            )
            grade += score * charm["skills"][skill]

        for slot in charm["slots"]:
            if slot == 0:
                break

            grade += slotValue[slot - 1]

        charm["grade"] = grade

    return charms


# main body
try:
    charms = json.load(open("charms.json", "r"))
    skillToJewel = json.load(open(os.path.join("data", "skillsToJewel.json"), "r"))
    scoreSkills = json.load(open(os.path.join("data", "skillsRank.json"), "r"))

    # get skills we don't care
    with open(os.path.join("data", "trashSkills.txt")) as f:
        content = f.read()
    f.close()

    trashSkills = list(content.split("\n"))
    trashSkills = list(filter(lambda skill: skill != "", trashSkills))

    charms = charmsGrader(charms)

    # add trash key quickly
    for index, charm in enumerate(charms):
        if len(charm["skillsLst"]) == 0:
            charm["trash"] = True
        else:
            charm["trash"] = False

    # compare each charm and add to rebirth list
    for i in range(len(charms) - 1):
        if charms[i]["trash"]:
            continue

        for j in range(i + 1, len(charms)):
            if charms[j]["trash"]:
                continue

            if isCharm1InCharm2(charms[i], charms[j], skillToJewel):
                charms[i]["trash"] = True
                print(
                    f"conserve {json.dumps(charms[j], indent=3)}\n== et jete ==\n{json.dumps(charms[i], indent=3)}"
                )
                break

            if isCharm1InCharm2(charms[j], charms[i], skillToJewel):
                charms[j]["trash"] = True
                print(
                    f"== conserve ==\n{json.dumps(charms[i], indent=3)}\n== et jete ==\n{json.dumps(charms[j], indent=3)}"
                )

    charms = sorted(charms, key=lambda charm: charm["grade"])
    charmsToRebirth = list(filter(lambda charm: charm["trash"], charms))

    # remove skillsLst it useless now
    for charm in charms:
        charm.pop("skillsLst", None)
        charm.pop("trash", None)

    for charm in charmsToRebirth:
        charm.pop("skillsLst", None)
        charm.pop("trash", None)

    charmsRanked = {
        "weak": list(filter(lambda charm: charm["grade"] < 2001, charms)),
        "low-average": list(filter(lambda charm: 2000 < charm["grade"] < 5001, charms)),
        "average": list(filter(lambda charm: 5000 < charm["grade"] < 10001, charms)),
        "good": list(filter(lambda charm: 10000 < charm["grade"] < 15001, charms)),
        "strong": list(filter(lambda charm: 15000 < charm["grade"] < 20001, charms)),
        "god": list(filter(lambda charm: 20000 < charm["grade"], charms)),
    }

    with open("charms.rebirth.json", "w") as f:
        json.dump(charmsToRebirth, f)
        f.close()

    with open("charms.ranked.json", "w") as f:
        json.dump(charmsRanked, f)
        f.close()


except Exception as e:
    print("something goes wrong :\n{}".format(e))
