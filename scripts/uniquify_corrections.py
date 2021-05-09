
with open("skill_corrections.csv", "r", encoding="utf-8") as csv:
    lines = csv.readlines()

with open("skill_corrections.csv", "w", encoding="utf-8") as csv:
    for line in sorted(set(lines), key=lambda x: x.split(",")[-1]):
        csv.write(line)
