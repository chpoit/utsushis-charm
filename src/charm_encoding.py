import json
from .Charm import Charm, CharmList


def encode_charms(charm_file, charm_encoded):
    charms = CharmList.from_file(charm_file)

    with open(charm_encoded, "w", encoding="utf-8") as encoded_file:
        encoded_charms = charms.encode_all()
        encoded_file.write(encoded_charms)

    return encoded_charms
