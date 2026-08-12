# -*- coding: utf-8 -*-
"""기존 기능 회귀 + 신규 매핑 무결성 자동 검사."""
import json
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
fail = []
warn = []


def ok(msg):
    print(f"  ✔ {msg}")


def bad(msg):
    fail.append(msg)
    print(f"  �’ {msg}")


def wrn(msg):
    warn.append(msg)
    print(f"  ! {msg}")


print("[1] JSON 파싱")
data = {}
for name in ("toc", "actuary", "kics", "dart-mapping"):
    try:
        with open(f"data/{name}.json", encoding="utf-8") as f:
            data[name] = json.load(f)
        ok(f"data/{name}.json 정상")
    except Exception as e:
        bad(f"data/{name}.json 파싱 실패: {e}")

toc, act, kics, mapping = data.get("toc"), data.get("actuary"), data.get("kics"), data.get("dart-mapping")

print("\n[2] 기존 구조 보존 (회귀)")
n_ifrs = sum(len(s["items"]) for ch in toc["chapters"] for s in ch["sections"])
n_act = sum(len(p["items"]) for ch in act["chapters"] for p in ch["parts"])
n_kics = sum(len(ch["items"]) for ch in kics["chapters"])
print(f"     IFRS17 {n_ifrs}항목 / 보험수리학 {n_act}항목 / K-ICS {n_kics}항목")
if n_ifrs == 48:
    ok("IFRS17 48항목 유지")
else:
    bad(f"IFRS17 항목수 변동: {n_ifrs} (기대 48)")
if n_act == 184:
    ok("보험수리학 184항목 유지")
else:
    bad(f"보험수리학 항목수 변동: {n_act} (기대 184)")
if n_kics == 61:
    ok("K-ICS 61항목 유지")
else:
    bad(f"K-ICS 항목수 변동: {n_kics} (기대 61)")

print("\n[3] toc id 무결성")
ids = [it.get("id") for ch in toc["chapters"] for s in ch["sections"] for it in s["items"]]
if all(ids) and len(set(ids)) == len(ids):
    ok(f"{len(ids)}개 id 모두 존재·고유")
else:
    bad("toc id 누락 또는 중복")

print("\n[4] dart-mapping 참조 ID가 실제로 존재하는지")
toc_ids = set(ids)
act_keys = set()
for ch in act["chapters"]:
    for p in ch["parts"]:
        for it in p["items"]:
            act_keys.add(f"{ch['num']}:{it['num']}")
kics_nums = {c["num"] for c in kics["chapters"]}

bad_ifrs, bad_act, bad_kics = [], [], []
entries = list(mapping["exact"].items()) + [(m.get("label", "keyword"), m) for m in mapping["keyword"]]
for label, m in entries:
    for i in m.get("ifrs17", []):
        if i not in toc_ids:
            bad_ifrs.append(f"{label} -> {i}")
    for a in m.get("actuarial", []):
        if a not in act_keys:
            bad_act.append(f"{label} -> {a}")
for label, m in mapping.get("kics", {}).items():
    for s in m.get("kicsSections", []):
        if s not in kics_nums:
            bad_kics.append(f"{label} -> {s}")
    for a in m.get("actuarial", []):
        if a not in act_keys:
            bad_act.append(f"{label} -> {a}")

if not bad_ifrs:
    ok("매핑의 ifrs17 id 전부 실제 존재")
else:
    bad(f"존재하지 않는 ifrs17 id: {bad_ifrs}")
if not bad_act:
    ok("매핑의 보험수리학 key 전부 실제 존재")
else:
    bad(f"존재하지 않는 보험수리학 key: {bad_act}")
if not bad_kics:
    ok("매핑의 K-ICS 장번호 전부 실제 존재")
else:
    bad(f"존재하지 않는 K-ICS 장: {bad_kics}")

print("\n[5] 원문 이미지 존재 (PDF 뷰어 회귀)")
for mode, cnt_key in (("ifrs17", "ifrs17"),):
    total = toc["pageCounts"][cnt_key]
    missing = [i for i in range(total) if not os.path.exists(f"images/ifrs17/{i:04d}.jpg")]
    if missing:
        bad(f"ifrs17 이미지 {len(missing)}장 누락 (예: {missing[:3]})")
    else:
        ok(f"ifrs17 원문 이미지 {total}장 전부 존재")
ktotal = kics["pageCounts"]["kics"] if "kics" in kics["pageCounts"] else None
if ktotal:
    kmissing = [i for i in range(ktotal) if not os.path.exists(f"images/kics/{i:04d}.jpg")]
    if kmissing:
        bad(f"kics 이미지 {len(kmissing)}장 누락")
    else:
        ok(f"K-ICS 원문 이미지 {ktotal}장 전부 존재")

print("\n[6] 수식 LaTeX 괄호 균형 (KaTeX 렌더 회귀)")
def unbalanced(s):
    depth = 0
    i = 0
    while i < len(s):
        if s[i] == "\\":
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

broken = []
for ch in act["chapters"]:
    for p in ch["parts"]:
        for it in p["items"]:
            for label, s in [("formula", it.get("formula", ""))] + [
                (f"deriv{i}", st.get("eq", "")) for i, st in enumerate(it.get("derivationSteps") or [])
            ]:
                if s and unbalanced(s):
                    broken.append(f"Ch{ch['num']} {it['num']} {label}")
if broken:
    bad(f"중괄호 불균형 수식 {len(broken)}건: {broken[:5]}")
else:
    ok("전체 수식 중괄호 균형 정상")

print("\n[7] Bridge 품질 규칙")
noevid = []
for ch in act["chapters"]:
    for p in ch["parts"]:
        for it in p["items"]:
            f = it.get("ifrs17") or {}
            if f.get("strength") == "직접적인 수리적 기반" and not f.get("note"):
                noevid.append(f"Ch{ch['num']} {it['num']}")
if noevid:
    bad(f"근거 없이 '직접적인 수리적 기반' 주장: {noevid}")
else:
    ok("'직접적인 수리적 기반' 주장은 모두 근거 서술 보유")

csm_items = [
    (ch["num"], it["num"], (it.get("ifrs17") or {}))
    for ch in act["chapters"]
    for p in ch["parts"]
    for it in p["items"]
    if "CSM" in it.get("title", "")
]
for cnum, num, f in csm_items:
    if f.get("strength") == "직접적인 수리적 기반":
        bad(f"CSM 항목 Ch{cnum} {num} 이 '직접적인 수리적 기반'으로 표시됨(전통 보험수리 공식과 동일시 위험)")
    elif not f.get("boundary"):
        wrn(f"CSM 항목 Ch{cnum} {num} 에 연결의 한계(boundary) 설명 없음")
    else:
        ok(f"CSM 항목 Ch{cnum} {num}: {f.get('strength')} / {f.get('nature')} + 한계 명시")

print("\n[8] 파일 존재 (신규 모드)")
for f in ("company.js", "api/companies.js", "api/ifrs17.js", "api/kics.js",
          "api/lib/dart.js", "api/lib/kics-parser.js", "api/lib/ifrs17-accounts.js",
          "api/lib/insurers.js", "api/lib/cors.js"):
    if os.path.exists(f):
        ok(f)
    else:
        bad(f"{f} 없음")

print("\n[9] API Key 노출 검사")
leaked = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "images", "scripts_audit")]
    for fn in files:
        if fn.endswith((".js", ".json", ".html", ".css")):
            path = os.path.join(root, fn)
            try:
                txt = open(path, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            if re.search(r"[0-9a-f]{40}", txt):
                leaked.append(path)
if leaked:
    bad(f"40자 hex(API key 형태) 문자열 발견: {leaked}")
else:
    ok("배포 대상 파일에 API key 형태 문자열 없음")

print("\n" + "=" * 60)
print(f"실패 {len(fail)}건 / 경고 {len(warn)}건")
for f in fail:
    print("  실패:", f)
for w in warn:
    print("  경고:", w)
sys.exit(1 if fail else 0)
