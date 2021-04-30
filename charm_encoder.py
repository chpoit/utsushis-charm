
import base64
import json

from Charm import Charm


charm_file = "charms.json"

with open(charm_file) as cf:
    charms = json.load(cf)


unique_charms = set()

for charm in map(Charm.from_dict, charms):
    unique_charms.add(charm)

print(len(charms), len(unique_charms))

def convert_list(charms):
    strung_up = ""
    
a = "Ci0KFAoQQWZmaW5pdHkgU2xpZGluZxADCg0KCUdvb2QgTHVjaxABGgYIAxACGAEKKwoUChBBZmZpbml0eSBTbGlkaW5nEAIKDQoJR29vZCBMdWNrEAEaBAgCEAIKLQoUChBBZmZpbml0eSBTbGlkaW5nEAEKDQoJR29vZCBMdWNrEAEaBggBEAEYAQonChQKEEFmZmluaXR5IFNsaWRpbmcQBAoNCglHb29kIEx1Y2sQARoA"

b = base64.b64decode(a)

print(b)
print()
# print(b.decode('ascii'))

q = b"""\n-\n\x14\n\x10Affinity Sliding\x10\x03\n\r\n\tGood Luck\x10\x01\x1a\x06\x08\x03\x10\x02\x18\x01\n+\n\x14\n\x10Affinity Sliding\x10\x02\n\r\n\tGood Luck\x10\x01\x1a\x04\x08\x02\x10\x02\n-\n\x14\n\x10Affinity Sliding\x10\x01\n\r\n\tGood Luck\x10\x01\x1a\x06\x08\x01\x10\x01\x18\x01\n'\n\x14\n\x10Affinity Sliding\x10\x04\n\r\n\tGood Luck\x10\x01\x1a\x00"""

q = b"""-\x14\x10Affinity Sliding\x10\x03Good Luck\x10\x01\x1a\x06\x08\x03\x10\x02\x18\x01+\x14\x10Affinity Sliding\x10\x02Good Luck\x10\x01\x1a\x04\x08\x02\x10\x02-\x14\x10Affinity Sliding\x10\x01Good Luck\x10\x01\x1a\x06\x08\x01\x10\x01\x18\x01'\x14\x10Affinity Sliding\x10\x04Good Luck\x10\x01\x1a\x00"""

z = base64.b64encode(q)
print(z)