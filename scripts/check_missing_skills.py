import os

all_skills = set()
with open('skill_list.txt') as slf:
    for line in slf.readlines():
        skill_name = line.strip()
        all_skills.add(skill_name)

existing = set()
for s_f in os.scandir(os.path.join("images","skills")):
    skill = s_f.name.split(".")[0]
    existing.add(skill)

missing = all_skills.symmetric_difference(existing)

for skill in sorted(missing):
    print(f"- {skill}")

print(missing)