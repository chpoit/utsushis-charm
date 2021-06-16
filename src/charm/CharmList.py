from . import Charm, InvalidCharm, GradedCharm


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

    def __add__(self, other):
        ns = CharmList()
        for item in self:
            ns.add(item)
        for item in other:
            ns.add(item)
        return ns

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
        if not (
            type(obj) == Charm or type(obj) == InvalidCharm or type(obj) == GradedCharm
        ):
            raise TypeError("Items must be charms")

    def has_invalids(self):
        return any(filter(lambda x: type(x) == InvalidCharm, self))
