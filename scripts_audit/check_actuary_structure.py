import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("data/actuary.json", encoding="utf-8") as f:
    d = json.load(f)

REQUIRED = [
    ("def", "정의"),
    ("symbols", "기호"),
    ("assumptions", "전제"),
    ("formula", "핵심수식"),
    ("derivationSteps", "도출과정"),
    ("termMeanings", "각항의미"),
    ("intuition", "직관"),
    ("relatedFormulas", "관련공식"),
    ("prerequisites", "선수개념"),
    ("leadsTo", "다음개념"),
    ("ifrs17", "IFRS17연결"),
    ("page", "출처(교재페이지)"),
]

def is_empty(v):
    if v is None:
        return True
    if isinstance(v, (list, dict, str)) and len(v) == 0:
        return True
    return False

total_items = 0
missing_counts = {k: 0 for k, _ in REQUIRED}
missing_detail = {k: [] for k, _ in REQUIRED}
per_chapter_rows = []

for ch in d["chapters"]:
    ch_total = 0
    ch_missing = {k: 0 for k, _ in REQUIRED}
    for part in ch.get("parts", []):
        for item in part.get("items", []):
            total_items += 1
            ch_total += 1
            label = f"Ch{ch['num']}-{item.get('num')} {item.get('title')}"
            for key, _ in REQUIRED:
                if key not in item or is_empty(item.get(key)):
                    missing_counts[key] += 1
                    ch_missing[key] += 1
                    if len(missing_detail[key]) < 40:
                        missing_detail[key].append(label)
    per_chapter_rows.append((ch['num'], ch['title'], ch_total, ch_missing))

print("=" * 70)
print(f"TOTAL ITEMS: {total_items}")
print("=" * 70)
print("\n[전체 필드별 누락 개수]")
for key, kor in REQUIRED:
    pct = missing_counts[key] / total_items * 100 if total_items else 0
    print(f"  {kor:20s} ({key:16s}): 누락 {missing_counts[key]:3d}개 / {total_items}개 ({pct:5.1f}%)")

print("\n[챕터별 누락 현황 - 누락 있는 필드만]")
for num, title, ch_total, ch_missing in per_chapter_rows:
    nonzero = {k: v for k, v in ch_missing.items() if v > 0}
    if nonzero:
        parts = ", ".join(f"{k}:{v}" for k, v in nonzero.items())
        print(f"  Ch{num} {title} (총 {ch_total}개): {parts}")
    else:
        print(f"  Ch{num} {title} (총 {ch_total}개): 누락 없음")

print("\n[필드별 누락 상세 (최대 40개씩)]")
for key, kor in REQUIRED:
    if missing_detail[key]:
        print(f"\n  --- {kor} ({key}) 누락 항목 ---")
        for label in missing_detail[key]:
            print(f"    - {label}")
