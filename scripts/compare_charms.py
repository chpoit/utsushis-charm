import os 
import sys
import json
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Charm import Charm

f1 = "charms tesseract.json"
f2 = "charms.json"

with open(f1) as f:
    c1 = set(map(Charm.from_dict,json.load(f)))

with open(f2) as f:
    c2 = set(map(Charm.from_dict,json.load(f)))

c1 = set(c1)
c2 = set(c2)

print(len(c1), len(c2), len(c1) == len(c2))

dif = c1.symmetric_difference(c2)

print("Diffs",  len(dif))

a =b=0
with open("missing_charms.json", "w", encoding="utf-8") as missing,\
    open("made_up_charms.json", "w", encoding="utf-8") as made_up:
    for i in dif:
        if i not in c1:
            a+=1
            made_up.write(f"{i.to_dict()}\n")
        else:
            b+=1
            missing.write(f"{i.to_dict()}\n")

print(f"Missing: {a}")
print(f"Made up: {b}")
