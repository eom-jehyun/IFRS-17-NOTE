# -*- coding: utf-8 -*-
"""δ(delta) 기호가 어디서 어떤 의미로 쓰였는지 전수 조사한다."""
import json
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/actuary.json", encoding="utf-8") as f:
    d = json.load(f)

DELTA = re.compile(r"\\delta|δ")

# (1+δ) 형태 = 실이율(effective rate)로 쓰는 용법
EFFECTIVE = re.compile(r"\(\s*1\s*\+\s*(\\delta|δ)")
# e^{δ}, exp(δ), /δ, ln 관련 = 이력(force)으로 쓰는 용법
FORCE = re.compile(r"e\^\{?\s*[-]?\s*(\\delta|δ)|\\frac\{[^}]*\}\{\\delta\}|\{\\delta\}|\\ln\(1\+i\)")

rows = []
for ch in d["chapters"]:
    for part in ch["parts"]:
        for it in part["items"]:
            hits = []
            f = it.get("formula", "") or ""
            if DELTA.search(f):
                hits.append(("formula", f))
            for i, st in enumerate(it.get("derivationSteps") or []):
                eq = st.get("eq", "") or ""
                if DELTA.search(eq):
                    hits.append((f"deriv{i}", eq))
            for s in it.get("symbols") or []:
                if DELTA.search(s.get("sym", "")):
                    hits.append(("symbol", f"{s.get('sym')} = {s.get('meaning')}"))
            for t in it.get("termMeanings") or []:
                if DELTA.search(t.get("term", "")):
                    hits.append(("term", f"{t.get('term')} = {t.get('meaning')}"))
            if hits:
                rows.append((ch["num"], it["num"], it["title"], hits))

print(f"δ 를 사용하는 항목: {len(rows)}개\n")
eff_items, force_items, unclear = [], [], []
for cn, num, title, hits in rows:
    kinds = set()
    for _, txt in hits:
        if EFFECTIVE.search(txt):
            kinds.add("실이율(1+δ)")
        if FORCE.search(txt):
            kinds.add("이력(force)")
    label = " + ".join(sorted(kinds)) if kinds else "판별필요"
    print(f"[Ch{cn} {num}] {title}")
    print(f"    용법판정: {label}")
    for where, txt in hits:
        print(f"      · {where}: {txt[:150]}")
    print()
    if "실이율(1+δ)" in kinds:
        eff_items.append(f"Ch{cn} {num}")
    if "이력(force)" in kinds:
        force_items.append(f"Ch{cn} {num}")
    if not kinds:
        unclear.append(f"Ch{cn} {num}")

print("=" * 66)
print(f"이력(force)으로 사용 : {len(force_items)}개 -> {force_items}")
print(f"실이율(1+δ)로 사용   : {len(eff_items)}개 -> {eff_items}")
print(f"기계판별 불가        : {len(unclear)}개 -> {unclear}")
if force_items and eff_items:
    print("\n>>> 동일 기호 δ 가 서로 다른 의미(이력 vs 실이율)로 혼용되고 있음")
