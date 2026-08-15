# -*- coding: utf-8 -*-
"""두 actuary.json 사이에서 특정 항목의 변경점을 보여준다. 인자: <old.json> <장번호> <항목num>"""
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

old_path, chnum, num = sys.argv[1], int(sys.argv[2]), sys.argv[3]

with open(old_path, encoding="utf-8") as f:
    old = json.load(f)
with open("data/actuary.json", encoding="utf-8") as f:
    new = json.load(f)


def find(doc):
    for ch in doc["chapters"]:
        if ch["num"] != chnum:
            continue
        for part in ch["parts"]:
            for item in part["items"]:
                if item["num"] == num:
                    return item
    return None


a, b = find(old), find(new)
if a is None or b is None:
    print("항목을 찾지 못했습니다.")
    sys.exit(1)

for key in ("formula", "def", "intuition", "relatedFormulas", "derivation"):
    if a.get(key) != b.get(key):
        print(f"[{key}]")
        print(f"  BEFORE: {a.get(key)}")
        print(f"  AFTER : {b.get(key)}\n")

for label in ("derivationSteps", "symbols", "termMeanings", "assumptions"):
    ja = json.dumps(a.get(label), ensure_ascii=False)
    jb = json.dumps(b.get(label), ensure_ascii=False)
    if ja != jb:
        print(f"[{label}]")
        print(f"  BEFORE: {ja[:900]}")
        print(f"  AFTER : {jb[:900]}\n")
