class Slots:
    def __init__(self, *slots):
        if type(slots[0]) is list:
            slots = slots[0]
        slots = list(slots)
        slots += [0] * 3
        slots = slots[:3]
        self.slots = list(sorted(slots, reverse=True))

    def to_simple_encode(self):
        return f"{self.slots[0]},{self.slots[1]},{self.slots[2]}"

    def has_slots(self, *slots):
        temp_copy = [slot for slot in self.slots]
        for slot in slots:
            if slot not in temp_copy:
                return False
            try:
                temp_copy.remove(slot)
            except IndexError:
                return False

        return True

    def __eq__(self, other):
        return (
            self.slots[0] != other.slots[0]
            or self.slots[1] != other.slots[1]
            or self.slots[2] != other.slots[2]
        )

    def __iter__(self):
        for slot in self.slots:
            yield slot

    def __str__(self):
        return f"{self.slots[0]}-{self.slots[1]}-{self.slots[2]}"

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(list(filter(lambda x: x > 0, self.slots)))
