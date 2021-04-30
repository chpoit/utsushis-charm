import json


class Charm:

    def __init__(self, slots, skills=None):
        if not skills:
            skills = {}
        self.slots = slots
        self.skills = skills

    def __eq__(self, other):
        return self.is_identical(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        hashcumulator = ""
        for i in self.slots:
            hashcumulator += str(hash(i))
        for s in self.skills:
            k = self.skills[s]
            hashcumulator += str(hash(f"{s}_{k}"))
        return hash(hashcumulator)

    def add_skill(self, skill, level):
        self.skills[skill.strip()] = level

    @staticmethod
    def from_dict(json_data):
        return Charm(json_data['slots'], json_data['skills'])

    def to_dict(self):
        return {'slots': self.slots, 'skills': self.skills}

    def is_identical(self, charm):
        if self.slots[0] != charm.slots[0] and\
            self.slots[1] != charm.slots[1] and\
                self.slots[2] != charm.slots[2]:
            return False

        if len(self.skills) != len(charm.skills):
            return False

        for skill in self.skills:
            if skill not in charm.skills or\
                    self.skills[skill] != charm.skills[skill]:
                return False

        return True

    def to_wonkyb64(self):
        # MONKEY BRAIN GOES BRRRRRRRRRRRRRR
        # Appears to be some weird b64 encoding and reversing minified code is not something I want to spend a weekend on
        # \x1a\x06\x08\x03\x10\x01\x18\x01 3-1-1
        # \x1a\x06\x08\x03\x10\x01\x18\x01 3-2-1
        # \x1a\x04\x08\x02\x10\x02 2-2-0
        # \x1a\x06\x08\x01\x10\x01\x18\x01 1-1-1
        # \x1a\x00 0-0-0
        def encode_slots(slots):
            slot_count = sum(x != 0 for x in slots)
            slot_codes = [
                "\\x00",
                "\\x02",
                "\\x04",
                "\\x06"]

            slot_position = ["\\x08", "\\x10", "\\x18"]

            pos = 0
            s = f"\\x1a{slot_codes[slot_count]}"
            for slot in slots:
                s += f"{slot_position[pos]}\\x0{slot}"
                pos += 1
            return s

        def encode_skills(skills):
            acc = ""
            skill_no = 0
            for skill in skills:
                if skill_no>0:
                    acc += "\\n\\r\\n\\t"
                level= self.skills[skill]
                acc+=f"{skill}\\x10\\x0{level}"
                skill_no+=1
            return acc

        k = "\\n+\\n\\x14\\n\\x10"    
        k += encode_skills(self.skills)
        k += encode_slots(self.slots)
        return k
