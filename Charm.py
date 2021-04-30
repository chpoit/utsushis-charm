import json


class Charm:

    def __init__(self, slots, skills=None):
        if not skills:
            skills ={}
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
        for skill in self.skills:
            k = f"{skill}\\x10\\x0{self.skills[skill]}\\n\\r\\n\\t"
            print(k)
        
