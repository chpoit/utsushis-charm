import json
from .Charm import Charm


def encode_charms(charm_file, charm_encoded):
    with open(charm_file) as cjsf:
        charms = json.load(cjsf)
    with open(charm_encoded, "w") as encoded:
        for charm in map(Charm.from_dict, charms):
            encoded.write(f"{charm.to_simple_encode()}\n")


if __name__ == "__main__":
    charm_file = "charms.json"
    encode_charms(charm_file)
