import json
from ..parse_errors import ParseError
from . import CharmGrade, Charm


class GradedCharm(Charm):
    def __init__(self, charm: Charm, grade: CharmGrade):
        super().__init__(charm.slots, charm.skills, charm.frame_loc)
        self.grade = grade

    def __hash__(self):
        hashcumulator = str(super().__hash__())
        hashcumulator += str(hash(self.grade))
        return hash(hashcumulator)

    @staticmethod
    def from_dict(json_data):
        if not "grade" in json_data:
            raise ValueError("Grade should be included in json data")
        return GradedCharm(
            Charm(json_data["slots"], json_data["frame"], json_data["skills"]),
            CharmGrade(json_data["grade"]),
        )

    def to_dict(self):
        return {
            "slots": self.slots,
            "skills": self.skills,
            "frame": self.frame,
            "grade": int(self.grade),
        }
