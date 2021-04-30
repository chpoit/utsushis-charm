
import base64
import json

from Charm import Charm


charm_file = "charms.json"

with open(charm_file) as cf:
    charms = json.load(cf)


unique_charms = set()

for charm in map(Charm.from_dict, charms):
    unique_charms.add(charm)


with open(charm_file, "w") as cf:
    json.dump(list(map(Charm.to_dict, unique_charms)), cf)

print(len(charms), len(unique_charms))

def convert_list(charms):
    strung_up = ""
    
a = "Ci4KEAoMQmxhc3QgQXR0YWNrEAEKEgoOSGVsbGZpcmUgQ2xvYWsQAhoGCAIQAhgBCjAKDwoLQ2FydmluZyBQcm8QAQoVChFXaXJlYnVnIFdoaXNwZXJlchABGgYIAxACGAE="

b = base64.b64decode(a)

print(b)
print()
# print(b.decode('ascii'))

charm_list = [Charm([2,2,1], {"Blast Attack":1, "Hellfire Cloak":2})]

for charm in charm_list:
    w = charm.to_wonkyb64()
    print("s", w)

    print()

q1 = b"""\n'\n\x10\n\x0cAffinity Sliding\x10\x03\n\r\n\tHellfire Cloak\x10\x02\x1a\x06\x08\x02\x10\x02\x18\x01\n0\n\x0f\n\x0bCarving Pro\x10\x01\n\x15\n\x11Wirebug Whisperer\x10\x01\x1a\x06\x08\x03\x10\x02\x18\x01"""

# Good Luck\x10\x02\x1a\x04\x08\x02\x10\x02
# Blast Attack\x10\x01\n\r\n\t\x1a\x06\x08\x02\x10\x02\x18\x01

#\n+\n\x14\n\x10Blast Attack\x10\x01\n\r\n\tHellfire Cloak\x10\x02\x1a\x06\x08\x02\x10\x02\x18\x01
#\n(\n\x14\n\x10Affinity Sliding\x10\x01\n\x0c\n\x08Botanist\x10\x01\x1a\x02\x08\x03



print(base64.b64encode(q1))


q = b"""
\n\x1e\n\x14\n\x10
Affinity Sliding\x10\x01\x1a\x06\x08\x03\x10\x01\x18\x01
\n-\n\x14\n\x10
Affinity Sliding\x10\x03\n\r\n\tGood Luck\x10\x01 \x1a\x06\x08\x03\x10\x02\x18\x01
\n+\n\x14\n\x10
Affinity Sliding\x10\x02\n\r\n\tGood Luck\x10\x01 \x1a\x04\x08\x02\x10\x01\x18\x01
\n-\n\x14\n\x10
Affinity Sliding\x10\x01\n\r\n\tGood Luck\x10\x01 \x1a\x06\x08\x01\x10\x01\x18\x01
\n'\n\x14\n\x10
Affinity Sliding\x10\x04\n\r\n\tGood Luck\x10\x01 \x1a\x00"""

z = base64.b64encode(q)
print(z)