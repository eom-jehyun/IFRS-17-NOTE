# -*- coding: utf-8 -*-
"""K-ICS explain 블록의 LaTeX 괄호 균형과 보강 범위를 확인한다."""
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BACKSLASH = chr(92)


def unbalanced(s):
    depth = 0
    i = 0
    while i < len(s):
        if s[i] == BACKSLASH:
            i += 2
            continue
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth < 0:
                return True
        i += 1
    return depth != 0


with open("data/kics.json", encoding="utf-8") as f:
    k = json.load(f)

n = 0
bad = 0
for ch in k["chapters"]:
    for it in ch["items"]:
        ex = it.get("explain")
        if not ex:
            continue
        n += 1
        formula = ex.get("formula", "")
        broken = bool(formula) and unbalanced(formula)
        if broken:
            bad += 1
        tag = "BAD " if broken else "ok  "
        print(
            f"  {tag}{ch['num']}-{it['code']} {it['title'][:24]:<26}"
            f" 질문 {len(ex.get('questions', []))}개 | 근거 pageStart={ex.get('sourcePage')}"
            f" | 수식 {'있음' if formula else '없음'}"
        )
print(f"\nexplain 블록 {n}개, LaTeX 오류 {bad}건")
sys.exit(1 if bad else 0)
