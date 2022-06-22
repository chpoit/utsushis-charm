import os
import json
import sys

# Simplest way I found to update json pre-build

print(sys.argv)

new_version = sys.argv[-1]

if new_version is sys.argv[0]:
    print("Version was not updated")
    exit()

print("Writing", new_version, "to file")

with open(os.path.join("data", "versions.json"), "r") as f:
    versions = json.load(f)
versions["app"] = new_version
with open(os.path.join("data", "versions.json"), "w") as f:
    json.dump(versions, f, indent=4)
