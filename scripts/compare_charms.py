import os 
import sys
import json
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Charm import Charm

f1 = "charms tesseract.json"
f2 = "charms extreme.json"

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
for i in dif:
    if i not in c1:
        a+=1
        # print(f"Missing from {f1}:\t {i.to_dict()}")
    else:
        b+=1
        # print(f"Missing from {f2}:\t {i.to_dict()}")

print(f"Missing: {a}")
print(f"Made up: {b}")
