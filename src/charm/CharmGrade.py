from enum import IntEnum


class CharmGrade(IntEnum):
    Trash = 0
    Poor = 1
    Average = 2
    Good = 3
    Great = 4
    def __add__(self, other):
        other_type = type(other)
        score = self.value
        if other_type is CharmGrade:
            score += other.value
        if other_type is int:
            score += other
        score = max(score, 0)
        score = min(max(CharmGrade), score)
        return CharmGrade(score)
    def __sub__(self, other):
        return self + -other
