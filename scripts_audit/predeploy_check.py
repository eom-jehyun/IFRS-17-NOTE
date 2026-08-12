# -*- coding: utf-8 -*-
"""
배포 전 최종검사. 기존 회귀검사(regression_check.py)에 배포 관련 항목을 더한 것.
새 기능을 추가하지 않고 '배포 가능한 구조인가'만 확인한다.
"""
import io
import json
import os
import re
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
fail, warn = [], []


def ok(m):
    print(f"  PASS  {m}")


def bad(m):
    fail.append(m)
    print(f"  FAIL  {m}")


def wrn(m):
    warn.append(m)
    print(f"  WARN  {m}")


print("[A] 기존 회귀검사 실행")
r = subprocess.run([sys.executable, "scripts_audit/regression_check.py"], capture_output=True, text=True, encoding="utf-8")
if r.returncode == 0:
    ok("regression_check.py 전항목 통과")
else:
    bad("regression_check.py 실패 — 아래 출력 확인")
    print(r.stdout[-1500:])

print("\n[B] Vercel 배포 구조")
if os.path.exists("vercel.json"):
    v = json.load(open("vercel.json", encoding="utf-8"))
    md = (v.get("functions") or {}).get("api/*.js", {}).get("maxDuration")
    if md:
        ok(f"vercel.json에 maxDuration 명시({md}s) — 플랫폼 기본값 변화에 영향받지 않음")
    else:
        wrn("vercel.json에 maxDuration 미지정 — 플랫폼 기본값에 의존")
else:
    bad("vercel.json 없음")

# api/ 함수는 CommonJS 기본 export 형태여야 Vercel이 인식한다.
for f in sorted(os.listdir("api")):
    if not f.endswith(".js"):
        continue
    txt = open(f"api/{f}", encoding="utf-8").read()
    if re.search(r"module\.exports\s*=\s*async?\s*\(?", txt):
        ok(f"api/{f} — Vercel 함수 시그니처(module.exports) 정상")
    else:
        bad(f"api/{f} — module.exports 핸들러 없음")

pkg = json.load(open("package.json", encoding="utf-8"))
deps = pkg.get("dependencies", {})
if "adm-zip" in deps:
    ok(f"package.json 런타임 의존성 선언됨: adm-zip {deps['adm-zip']}")
else:
    bad("adm-zip 의존성 누락 — Vercel 빌드 시 설치되지 않음")
if os.path.exists("package-lock.json"):
    ok("package-lock.json 존재 (재현 가능한 설치)")
else:
    wrn("package-lock.json 없음")

print("\n[C] 백엔드 URL 단일 관리")
if not os.path.exists("config.js"):
    bad("config.js 없음")
else:
    cfg = open("config.js", encoding="utf-8").read()
    if "VERCEL_API_BASE" in cfg:
        ok("config.js에 VERCEL_API_BASE 단일 정의 존재")
    else:
        bad("config.js에 VERCEL_API_BASE 없음")

# 프론트 파일에서 vercel.app 주소가 config.js 외에 하드코딩되지 않았는지
hard = []
for f in ("app.js", "company.js", "index.html"):
    if os.path.exists(f) and "vercel.app" in open(f, encoding="utf-8").read():
        hard.append(f)
if hard:
    bad(f"백엔드 주소가 config.js 외에 중복 하드코딩됨: {hard}")
else:
    ok("app.js·company.js·index.html에 백엔드 주소 중복 없음")

# index.html이 config.js를 company.js보다 먼저 로드하는지
html = open("index.html", encoding="utf-8").read()
ci, coi = html.find("config.js"), html.find("company.js")
if ci != -1 and coi != -1 and ci < coi:
    ok("index.html 스크립트 로드 순서 정상 (config.js → company.js → app.js)")
else:
    bad("index.html에서 config.js가 company.js보다 먼저 로드되지 않음")

print("\n[D] localhost / 디버그 흔적 (배포 대상 파일 한정)")
DEPLOY_FILES = ["index.html", "app.js", "company.js", "config.js", "style.css"]
for f in DEPLOY_FILES:
    txt = open(f, encoding="utf-8").read()
    # config.js의 LOCAL_API_BASE는 의도된 개발용 분기이므로 허용
    hits = [m for m in re.findall(r"localhost|127\.0\.0\.1", txt)]
    if hits and f != "config.js":
        bad(f"{f}에 localhost 참조 {len(hits)}건 (배포본에 남으면 안 됨)")
    elif hits:
        ok(f"{f}의 localhost는 개발 분기용(LOCAL_API_BASE)으로 의도된 것")
    else:
        ok(f"{f} localhost 참조 없음")
    if re.search(r"console\.(log|debug)\s*\(", txt):
        wrn(f"{f}에 console.log 잔존")

print("\n[E] API Key 노출 (전체 배포 대상)")
leak = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "images", "scripts_audit")]
    for fn in files:
        if fn.endswith((".js", ".json", ".html", ".css", ".md")):
            p = os.path.join(root, fn)
            t = open(p, encoding="utf-8", errors="ignore").read()
            if re.search(r"[0-9a-f]{40}", t):
                leak.append(p)
if leak:
    bad(f"API key 형태(40자 hex) 문자열 발견: {leak}")
else:
    ok("배포 대상 전체에 API key 형태 문자열 없음")

gi = open(".gitignore", encoding="utf-8").read()
for pat in ("node_modules",):
    if pat in gi:
        ok(f".gitignore에 {pat} 포함")
    else:
        bad(f".gitignore에 {pat} 없음 — 저장소가 비대해짐")

# 키가 담긴 파일이 저장소 안에 없는지
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git")]
    for fn in files:
        if "인증키" in fn or fn in (".env", ".env.local"):
            bad(f"키 파일이 저장소 내부에 존재: {os.path.join(root, fn)}")
else:
    ok("저장소 내부에 인증키/.env 파일 없음")

print("\n[F] CORS 허용 origin")
cors = open("api/lib/cors.js", encoding="utf-8").read()
if "eom-jehyun.github.io" in cors:
    ok("GitHub Pages origin 명시적 허용")
else:
    bad("GitHub Pages origin이 허용목록에 없음")
if 'Access-Control-Allow-Origin", "*"' in cors:
    bad("CORS가 와일드카드(*)로 열려 있음")
else:
    ok("CORS 와일드카드 아님")
if re.search(r'setHeader\(\s*"Vary"\s*,\s*"Origin"', cors):
    ok("Vary: Origin 설정됨 (CDN이 origin별로 캐시 분리 — 캐시 오염 방지)")
else:
    bad("Vary: Origin 누락 — 제3자 요청이 캐시를 오염시켜 사이트가 차단될 수 있음")

print("\n" + "=" * 62)
print(f"FAIL {len(fail)}건 / WARN {len(warn)}건")
for x in fail:
    print("  FAIL:", x)
for x in warn:
    print("  WARN:", x)
print("판정:", "배포 가능" if not fail else "배포 불가 — FAIL 항목 해결 필요")
sys.exit(1 if fail else 0)
