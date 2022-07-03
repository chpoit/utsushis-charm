import os
import json
import pandas as pd


mappings = {
    "English": "eng",
    "Japanese": "jpn",
    "French": "fra",
    "Italian": "ita",
    "German": "deu",
    "Spanish": "spa",
    "Russian": "rus",
    "Polish": "pol",
    "Korean": "kor",
    "traditional Chinese": "chi_tra",
    "Simplified Chinese": "chi_sim",
}


csv_path = os.path.join(".", "mh-rise skills language - Feuille 1.csv")

sp = os.path.join("data", "skills")
os.makedirs(sp, exist_ok=True)
skill_source = "English"
content = pd.read_csv(csv_path)

skills = {mappings[key]: {} for key in mappings}
skills_reverse = {mappings[key]: {} for key in mappings}
freqs = {mappings[key]: {} for key in mappings}

for index, row in content.iterrows():
    source_name = row[skill_source]
    for header in mappings:
        lang_code = mappings[header]
        skill_name = row[header]
        skills[lang_code][skill_name] = source_name
        skills_reverse[lang_code][source_name] = skill_name
        words = skill_name.split()
        for word in words:
            if not word in freqs[lang_code]:
                freqs[lang_code][word] = 0
            freqs[lang_code][word] += 1


for lang_code in mappings.values():
    skill_file = os.path.join(sp, f"skills.{lang_code}.txt")
    freq_file = os.path.join(sp, f"skills.{lang_code}.freq")
    corrections_file = os.path.join(sp, f"corrections.{lang_code}.csv")
    with open(skill_file, "w", encoding="utf-8") as skill_fp:
        for s_n in sorted(skills[lang_code]):
            skill_fp.write(f"{s_n}\n")

    old_corrections = []
    with open(corrections_file, "r", encoding="utf-8") as corrections_fp:
        old_corrections = list(
            map(
                lambda l: l.strip().split(",")[0],
                filter(lambda l: not not l, corrections_fp.readlines()),
            )
        )

    with open(freq_file, "w", encoding="utf-8") as freq_fp:
        for word in sorted(freqs[lang_code]):
            freq_fp.write(f"{word} {freqs[lang_code][word]}\n")

    with open(corrections_file, "w", encoding="utf-8") as corrections_fp:
        for word in sorted(set([n for n in freqs[lang_code]] + old_corrections)):
            corrections_fp.write(f"{word},{word}\n")


with open(
    os.path.join(sp, "skill_mappings.en.json"), "w", encoding="utf-8"
) as skill_map_fp:
    json.dump(skills_reverse, skill_map_fp, ensure_ascii=False)
with open(
    os.path.join(sp, "skill_mappings.alt.json"), "w", encoding="utf-8"
) as skill_map_fp:
    json.dump(skills, skill_map_fp, ensure_ascii=False)
