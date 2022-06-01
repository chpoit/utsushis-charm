from . import Charm


class InvalidCharm(Charm):
    def __init__(self, charm: Charm, skill_errors: [(list, str, int, ParseError)]):
        super().__init__(charm.slots, charm.skills, frame_loc=charm.frame_loc)
        self.skill_errors = skill_errors

    def get_errors(self):
        yield from self.skill_errors

    def repair(self, fixed_skills):
        return Charm(self.slots, fixed_skills, self.frame_loc)

    def to_dict(self):
        base = super().to_dict()
        simpler_errors = list(map(lambda x: list(map(str, x[1:])), self.skill_errors))
        base["errors"] = simpler_errors
        return base

    def has_skills(self):
        return True
