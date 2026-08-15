# 작업 인계 문서 (다음 Claude Code 세션용)

> 이 파일만 읽으면 이전 대화 맥락 없이도 이어서 작업할 수 있도록 정리한 것이다.
> 새 대화창에서 **"HANDOFF.md 읽고 이어서 작업해줘"** 라고 하면 된다.

---

## 1. 프로젝트가 무엇인가

**공개 링크**: https://eom-jehyun.github.io/IFRS-17-NOTE/
**저장소**: https://github.com/eom-jehyun/IFRS-17-NOTE (브랜치 `main`)
**로컬 경로**: `C:\Users\엄제현\Desktop\ifrs17-site-web`

보험회사의 회계수치·지급여력 수치가 **어떤 기준과 수리적 원리를 거쳐 만들어지는지 추적**할 수 있는 지식연결 사이트다.
단순 요약 사이트가 아니라 다음 흐름을 하나로 잇는 것이 목적이다.

```
보험회계해설서(IFRS17) → 보험수리학 → 둘의 Bridge → K-ICS → 실제 보험사 공시(DART)
```

**용도**: 삼일회계법인 자기소개서에 첨부하는 포트폴리오 링크. 회계사·계리사가 볼 것을 전제로 **정확성이 최우선**이다.

---

## 2. 기술 구조

- **프론트**: 순수 HTML/CSS/Vanilla JS 정적 사이트 (프레임워크 없음), GitHub Pages 배포
- **수식**: KaTeX (CDN)
- **백엔드**: Vercel 서버리스 함수 (`api/`) — DART 조회 전용
  - Production: `https://ifrs-17-note.vercel.app`
  - `DART_API_KEY`는 Vercel 환경변수에만 존재. 코드·저장소에 없음
  - 백엔드 주소는 **`config.js` 한 곳**에서만 관리 (중복 하드코딩 금지)
- **모드 4개**: IFRS17 해설서 / 최신보험수리학 / K-ICS / 보험사 분석

### 데이터 파일
| 파일 | 내용 |
|---|---|
| `data/toc.json` | IFRS17 해설서 48항목 (고유 id `ifrs-c{장}-s{절}-i{항}`) |
| `data/actuary.json` | 보험수리학 12장 184항목 ← **주 작업 대상** |
| `data/kics.json` | K-ICS 해설서 61항목 |
| `data/dart-mapping.json` | DART 계정 ↔ 해설서 ↔ 보험수리학 매핑 |

### 원문 자료 (저장소 밖)
`C:\Users\엄제현\Desktop\최신보험수리학\` 에 있음
- `최신보험수릭학 1(ocr).pdf` — 572p. **책 페이지 = PDF인덱스 − 26**
- `최신보험수릭학 2(ocr).pdf` — 782p. **책 페이지 = PDF인덱스 + 546**
- `IFRS17보험회계해설서_221116.pdf`, `新지급여력제도(K-ICS) 해설서.pdf`
- DART 키: `C:\Users\엄제현\Desktop\회계사 AI 교육 및 관련 아무거나\금감원 api 인증키.txt` (2번째 줄)

PDF 읽기는 `pymupdf` 사용:
```python
import pymupdf
d = pymupdf.open('최신보험수릭학 2(ocr).pdf')
print(d[책페이지 - 546 - 1].get_text())   # 2권
```

---

## 3. 반드시 지켜야 할 원칙

1. **교재 원문을 복제하지 않는다.** 설명문·예제 모두 이론을 이해한 바탕으로 새로 쓴다. 어미만 바꾸는 재작성도 안 된다.
2. **자료에 없는 내용을 만들지 않는다.** 확인 안 되면 "직접 대응 없음"으로 둔다. 이는 실패가 아니라 정확성 기능이다.
3. **CSM을 전통 보험수리 공식과 동일시하지 않는다.** 수리적 기반과 IFRS17 고유 회계처리를 분리 표시한다.
4. **K-ICS를 일반 재무제표로 추정하지 않는다.** 공시된 값만 쓴다.
5. **런타임 LLM API를 추가하지 않는다.** (사용자가 문제 사진 자동풀이 탭을 요청했으나 이 원칙·비용·공개남용·검증불가 이유로 **보류 결정**함)
6. **없는 값을 0으로 만들지 않는다.** '계정 확인 불가' / '공시 확인 불가' / '보고서 없음' / 'API 오류'를 구분한다.
7. **매 변경마다: 검사 통과 → commit → push → GitHub Pages 반영 확인**까지 한다. 사용자가 강조한 사항이다.

---

## 4. 검사 스크립트 (작업 전후 반드시 실행)

```bash
cd "C:/Users/엄제현/Desktop/ifrs17-site-web"
export PYTHONUTF8=1
python3 scripts_audit/predeploy_check.py      # 종합 (회귀+LaTeX+배포구조+키노출+CORS)
python3 scripts_audit/check_actuary_structure.py   # 184항목 필드 누락 현황
```

`predeploy_check.py`가 **FAIL 0건**이어야 push한다.

### 배포 확인 패턴
```bash
git add -A && git commit -q -m "..." && git push -q origin main
until curl -s -m 20 "https://eom-jehyun.github.io/IFRS-17-NOTE/data/actuary.json" | grep -q "새로추가한고유문자열"; do sleep 8; done
```

---

## 5. 현재 상태

### 완료된 것
- **보험수리학 184항목 12필드 전부 완비** (각 항의 의미 75%→0%, 기호 0.5%, 전제 0.5%)
- **교재 대조로 수식 오류 19건 수정** (Balducci, De Moivre 생명연금, δ 기호 3중 혼용, 9장 절대탈퇴율 방향, 11장 만기보험금 누락 등)
- Bridge 검수: '직접적인 수리적 기반' 55→42건 하향, `nature`/`boundary` 필드 신설
- K-ICS 이론 5개 절 보강 (해설서 근거 페이지 표시)
- 보험사 분석 모드: 상장 보험사 12곳, 최근 3개년 IFRS17 계정, K-ICS 표 추출, DART 원문 링크
- 프로덕션 E2E 검증 완료 (삼성생명·DB손해보험·현대해상·삼성화재)
- **최신보험수리학 3-서브탭 재편**(이론설명/공식정리/예제)

### 진행 중 — 다음 세션의 주 작업
사용자 요구: **"수험서처럼 훨씬 상세하게"**

각 항목에 다음 4개 필드를 채우는 작업이다.

| 필드 | 내용 |
|---|---|
| `narrative` | 절 단위 상세 전개. `{heading, text, cfTable, eq, after}` |
| `cfTable` | 시점별 현금흐름표 `{caption, headers, rows:[{label, cells}], note}` — 셀은 LaTeX 문자열(자동으로 `$..$` 감쌈) |
| `glossary` | 그 절 용어 전부 `{term, def}` |
| `formulaSummary` | 공식정리 탭용 `{name, eq, note}` |

**서술 규칙 (사용자가 명시한 것)**
- 시그마를 처음부터 쓰지 말 것. **각 항을 나열 → 등비수열 등으로 묶기 → 마지막에 시그마로 압축**
- **현금흐름표(시점 cf표)를 그려서** 공식이 표의 어느 칸을 더한 것인지 보이게 할 것
- 공식이 **어떻게 도출되는지** 빠짐없이 설명할 것
- 전개 후 **용어 정리**(부리·단리·복리 등 모든 단어)
- **공식 정리**도 담을 것

#### 진척도
- **1장 심화 완료**: I-1, I-3, I-6, I-8 (4/16)
- **1장 남음**: I-2, I-4, I-5, I-7, II-1~II-8 (12개)
- **2~12장 전부 남음**

#### 예제(`examples`) 진척도
- 1장 15개, 2장 5개, 3장 4개 = **24개 항목 완료**
- 4~12장 남음

**예제 작성 규칙**: 교재 예제 복제 금지. 스크립트 안에 `verify()`를 두어 본문의 모든 수치를 재계산해 대조하고, **불일치 시 적용 중단**시킬 것. 이 장치가 실제로 반올림 오차 2건을 잡았다.

---

## 6. 작업 패턴 (그대로 복제하면 됨)

`scripts_audit/deepen_ch1.py` 를 템플릿으로 삼는다.

```python
P = {}
P["I-2"] = {
    "narrative": [
        {"heading": "1. ...", "text": "...", "cfTable": {...}, "eq": r"...", "after": "..."},
    ],
    "glossary": [{"term": "...", "def": "..."}],
    "formulaSummary": [{"name": "...", "eq": r"...", "note": "..."}],
}
# main(): actuary.json 로드 → 해당 장 항목에 item.update(P[num]) → 저장
```

예제는 `scripts_audit/add_examples_ch1.py` 의 `verify()` 패턴을 복제한다.

### 권장 순서
1. **1장 나머지 12개 마저 심화** (일관성 위해 한 장을 끝내는 게 좋음)
2. 2장 → 3장 → … 순서대로
3. 각 장 끝날 때마다 검사 → push → 배포확인

---

## 7. 주의할 함정 (실제로 겪은 것들)

| 함정 | 대응 |
|---|---|
| `hidden` 속성이 CSS `display:flex`에 밀려 무효화 | `[hidden]{display:none!important}` 이미 추가됨 |
| 기호 치환 시 `\times\delta` → `\timesr` 같은 깨진 LaTeX | `check_latex_tokens.py`가 자동 검출 |
| JS 문자열에서 `"\("` 는 `"("` 가 됨 | cfTable은 `$..$` 델리미터 사용 |
| bash heredoc에 백틱·`${}` 섞으면 깨짐 | Python 스크립트를 **파일로** 작성해 실행 |
| Node가 Git Bash 경로(`/c/...`) 못 읽음 | Windows 경로(`C:/...`) 사용 |
| `pkill`이 Windows에서 안 먹힘 | PowerShell `Get-NetTCPConnection ... Stop-Process` |
| Python `print`에 한글 → cp949 오류 | `PYTHONUTF8=1` + `io.TextIOWrapper` |

---

## 8. 남은 개선 여지 (우선순위 낮음)

- `다음개념(leadsTo)` 46건 미기재 — 탐색 편의용
- KaTeX가 CDN 의존 — 기업 내부망 차단 시 수식이 원시 LaTeX로 보일 수 있음
- 브라우저 실물 확인 미완 — 도구가 `github.io`·`localhost`를 차단해 API·정적파일·소스 레벨로만 검증함. 사용자가 직접 확인 권장
- 통합검색(모드 교차) 미구현 — 선택사항이었음

---

## 9. 최근 커밋 (역순)

```
b31d5ed  최신보험수리학 3-서브탭 재편, 1장 기초이론 심화
f5ead6a  2~3장 예제 9개 추가
7a8d535  1장 예제 15개 추가 및 예제 렌더링 도입
1858d7b  10장 보강 — 184항목 각 항의 의미 완료
1f3d1b8  8~9장 보강 및 표기 문제 3건 해소
6c89659  4~7장 각 항의 의미 보강
db7d8bb  1~3장 각 항의 의미 보강
a5d2ca2  9장 절대탈퇴율 방향 오류 수정
1f3d1b8  12장 보강 및 KaTeX 렌더 깨짐 수정
e9763bf  δ 기호 혼용 해소
```
