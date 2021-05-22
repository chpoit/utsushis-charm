import json


class Charm:
    def __init__(self, slots, skills=None):
        if not skills:
            skills = {}
        self.slots = list(sorted(slots, reverse=True))
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
        return Charm(json_data["slots"], json_data["skills"])

    def to_dict(self):
        return {"slots": self.slots, "skills": self.skills}

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

        for level in self.slots:
            acc += f"{level},"
        return acc[:-1]

    def has_skills(self):
        return len(self.skills)


class CharmList(set):
    def __init__(self, *args, **kwargs):
        if args and len(args) > 0:
            for item in args[0]:
                self._test_item(item)
        super(CharmList, self).__init__(*args, **kwargs)

    def encode_all(self):
        acc = ""
        for charm in self:
            acc += f"{charm.to_simple_encode()}\n"
        return acc

    def to_json(self):
        return CharmList

    def add(self, item: Charm):
        self._test_item(item)
        super().add(item)

    def to_dict(self):
        return list(map(lambda x: x.to_dict(), self))

    @staticmethod
    def from_file(file_path):
        with open(file_path, "r", encoding="utf-8") as charm_file:
            data = json.load(charm_file)
        return CharmList.from_dict(data)

    @staticmethod
    def from_dict(charm_dict):
        new_list = CharmList()
        for item in charm_dict:
            new_list.add(Charm.from_dict(item))
        return new_list

    @staticmethod
    def _test_item(obj):
        if not type(obj) == Charm:
            raise TypeError("Items must be charms")
