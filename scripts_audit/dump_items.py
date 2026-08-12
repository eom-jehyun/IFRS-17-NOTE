"""지정한 항목들의 전체 JSON을 출력한다. 인자: Ch:num 형태 (예: 1:I-7 2:II-9)"""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
targets = set(sys.argv[1:])

with open("data/actuary.json", encoding="utf-8") as f:
    d = json.load(f)

for ch in d["chapters"]:
    for part in ch.get("parts", []):
        for it in part.get("items", []):
            key = f"{ch['num']}:{it.get('num')}"
            if key in targets:
                print(f"\n{'='*70}\n### {key}  [Ch{ch['num']} {ch['title']}]\n{'='*70}")
                print(json.dumps(it, ensure_ascii=False, indent=2))
