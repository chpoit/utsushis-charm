import json
from ..parse_errors import ParseError
from . import Slots


class Charm:
    def __init__(self, slots, skills=None, frame_loc=None):
        if not skills:
            skills = {}
        self.slots = Slots(slots)
        self.frame = frame_loc
        self.skills = skills
        self.frame_loc = frame_loc

    def __eq__(self, other):
        return self.is_identical(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        hashcumulator = str(hash(self.slots))
        for s in self.skills:
            k = self.skills[s]
            hashcumulator += str(hash(f"{s}_{k}"))
        return hash(hashcumulator)

    def add_skill(self, skill, level):
        self.skills[skill.strip()] = level

    @staticmethod
    def from_dict(json_data):
        return Charm(json_data["slots"], json_data["frame"], json_data["skills"])

    def to_dict(self):
        return {"slots": self.slots, "skills": self.skills, "frame": self.frame}

    def is_identical(self, charm):
        if (
            self.slots[0] != charm.slots[0]
            or self.slots[1] != charm.slots[1]
            or self.slots[2] != charm.slots[2]
        ):
            return False

        if len(self.skills) != len(charm.skills):
            return False

        for skill in self.skills:
            if skill not in charm.skills or self.skills[skill] != charm.skills[skill]:
                return False

        return True

    def to_simple_encode(self):
        acc = ""
        for skill in self.skills:
            acc += f"{skill},{self.skills[skill]},"
        if len(self.skills) == 0:  # should be impossible
            acc += ",0,"
        if len(self.skills) <= 1:
            acc += ",0,"

        acc += self.slots.to_simple_encode()
        return acc

    def has_skills(self):
        return len(self.skills)

    def has_slots(self, *slots):
        return self.slots.has_slots(*slots)

    def slot_count(self):
        return len(self.slots)
