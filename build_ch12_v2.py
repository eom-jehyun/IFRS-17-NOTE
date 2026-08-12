# -*- coding: utf-8 -*-
# 제12장 보험부채 변동분석과 손익인식 — 12-field schema. 마지막 핵심 장, 최대한 신중하게 작성.
import json

def sym(s, m):
    return {"sym": s, "meaning": m}

def term(t, m):
    return {"term": t, "meaning": m}

def ifrs(strength, items=None, note=None):
    d = {"strength": strength}
    if items:
        d["items"] = items
    if note:
        d["note"] = note
    return d

def step(text, eq=None):
    d = {"text": text}
    if eq:
        d["eq"] = eq
    return d

I = [
    {
        "num": "I-1", "title": "참가특성의 의미", "titleEn": "participation features", "page": 1164,
        "def": "계약자가 보험회사의 운용성과나 특정 기초항목(펀드 등)의 성과를 나눠 갖는 특성(참가특성)의 의미를 정의한다. 수학적으로는 급부가 확률변수(기초항목 성과)에 연동되는 구조이고, 보험수리학적으로는 6장 I-6의 금리연동형상품·11장 II-9의 보너스적립액이 이미 예고했던 개념을 회계처리 관점에서 공식화한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{급부} = f(\text{기초항목의 성과})",
        "derivationSteps": [
            step("6장 I-6에서 이미 다룬 '공시이율에 연동되는 계약자적립액', 11장 II-9의 '보너스적립액'이 바로 참가특성의 실제 사례였음을 재확인한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 장은 완전히 새로운 상품구조를 소개하는 것이 아니라, 6장·11장에서 이미 계산해본 금리연동형상품의 회계처리를 본격적으로 다루는 장이다.",
        "relatedFormulas": "6장 I-6, 11장 II-9의 재확인.",
        "prerequisites": ["6장 I-6 금리연동형보험의 계약자적립액", "11장 II-9 금리연동형상품의 사망보험금과 보너스적립액"],
        "leadsTo": ["I-2 참가특성 유무에 따른 회계모형의 종류"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.9 변동수수료모형"], "참가특성이라는 개념 자체가 해설서 4.9 변동수수료모형(VFA) 적용 여부를 가르는 핵심 판단기준이다."),
    },
    {
        "num": "I-2", "title": "참가특성 유무에 따른 회계모형의 종류", "page": 1165,
        "def": "일반모형(GMA)이 기본이며, 직접참가특성이 있는 계약(기초항목 성과와 연동)은 변동수수료접근법(VFA), 보장기간이 짧은 단기계약은 보험료배분접근법(PAA)을 선택 적용할 수 있다.",
        "symbols": [sym("GMA", "일반모형(General Model)"), sym("VFA", "변동수수료접근법(Variable Fee Approach)"), sym("PAA", "보험료배분접근법(Premium Allocation Approach)")],
        "assumptions": [],
        "formula": r"\text{계약} \to \begin{cases}\text{PAA} & \text{단기(보장기간}\le 1\text{년 등)}\\ \text{VFA} & \text{직접참가특성 O}\\ \text{GMA} & \text{그 외(기본)}\end{cases}",
        "derivationSteps": [
            step("보장기간이 짧아 GMA와 결과 차이가 미미한 계약은 단순화된 PAA를 쓸 수 있다(2장 4.10, 11장에서 다루지 않은 손해보험형 상품에 주로 해당).", None),
            step("직접참가특성 3요건(기초항목 몫 계약조건 명시, 공정가치 변동의 상당부분을 계약자에게 지급, 지급액의 상당부분이 기초항목 성과에 따라 변동)을 충족하면 VFA를 적용한다 — 11장 II-9의 UL종신보험이 전형적 사례다.", None),
            step("나머지 모든 계약(11장 II-8의 금리확정형 종신보험 등)은 GMA를 적용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "GMA와 VFA는 회계처리의 큰 틀(BEL+RA+CSM)은 동일하지만, VFA는 기초항목의 공정가치 변동을 손익이 아니라 CSM에서 흡수한다는 점이 다르다(I-3에서 상세히 다룸). PAA는 아예 BEL·CSM을 정교하게 계산하지 않는 단순화 방식이다.",
        "relatedFormulas": "I-1의 판단기준 실무화.",
        "prerequisites": ["I-1 참가특성의 의미"],
        "leadsTo": ["I-3 회계모형별 보험부채의 보험금융비용"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.8 회계모형", "IFRS17 4.9 변동수수료모형", "IFRS17 4.10 보험료배분접근법"], "해설서 2.8·4.9·4.10과 1:1로 대응된다."),
    },
    {
        "num": "I-3", "title": "회계모형별 보험부채의 보험금융비용", "page": 1167,
        "def": "GMA와 VFA에서 보험금융비용(할인 적용에 따른 이자부리 효과)을 계산하는 방식의 차이를 다룬다.",
        "symbols": [sym("δ", "할인율(1장 I-5, 11장 I-8)")],
        "assumptions": [],
        "formula": r"\text{GMA: 보험금융비용} = BEL\times\delta(\text{계약시점 할인율 고정 또는 현행 할인율}) \quad \text{VFA: 기초항목 변동을 CSM에서 흡수}",
        "derivationSteps": [
            step("GMA에서는 BEL에 할인율(11장 I-8)을 곱한 이자부리 효과가 보험금융비용으로 손익(또는 OCI)에 표시된다.", None),
            step("VFA에서는 기초항목의 공정가치 변동 중 계약자 몫에 해당하는 부분을 보험금융비용이 아니라 CSM 조정 항목으로 처리한다는 점이 GMA와 근본적으로 다르다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "VFA가 '보험금융손익 변동성을 CSM이 흡수하도록' 설계된 이유는, 참가특성 상품에서는 기초항목 성과 변동이 어차피 계약자에게 대부분 전가되므로 회사의 순손익에 그 변동성을 그대로 반영하는 것이 경제적 실질에 맞지 않기 때문이다.",
        "relatedFormulas": "I-2의 구체화.",
        "prerequisites": ["I-2 참가특성 유무에 따른 회계모형의 종류"],
        "leadsTo": ["I-4 IFRS17 손익 인식"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.9.3 주요 회계처리"]),
    },
    {
        "num": "I-4", "title": "IFRS17 손익 인식", "page": 1174,
        "def": "보험수익 = 그 기간 ①CSM 상각액 + ②RA의 위험소멸분 + ③예상발생보험금·사업비(실제가 아닌 '기대했던' 금액 기준) + ④보험취득현금흐름 상각액의 합. 이 네 요소를 더하면 '해당 기간 제공한 보험서비스의 대가'가 된다.",
        "symbols": [sym("CSM 상각액", "그 기간 제공한 서비스에 해당하는 CSM 인식분"), sym("RA 위험소멸분", "그 기간 경과에 따라 소멸한 위험조정")],
        "assumptions": ["GMA 기준"],
        "formula": r"\text{보험수익} = \Delta CSM_{\text{상각}} + \Delta RA_{\text{소멸}} + (\text{예상발생보험금+사업비}) + (\text{보험취득현금흐름 상각})",
        "derivationSteps": [
            step("6장 I-2에서 예고했던 'IFRS17은 보장을 제공한 시점에 맞춰 수익을 인식한다'는 원칙을 구체적인 산식으로 완성한다.", None),
            step("네 요소를 모두 더하면, 그 기간 실제 위험을 부담하고 서비스를 제공한 대가 전체가 수익으로 인식된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "IFRS4의 현금주의(수입보험료=수익)와 정반대되는 발생주의적 접근이라는 점이 핵심이다 — '보험료를 받은 시점'이 아니라 '보장을 제공한 시점'에 맞춰 수익을 인식한다.",
        "relatedFormulas": "6장 I-2에서 예고된 내용의 완성.",
        "prerequisites": ["6장 I-2 IFRS4 기준 책임준비금과 IFRS17 기준 책임준비금", "I-3 회계모형별 보험부채의 보험금융비용"],
        "leadsTo": ["I-5 IFRS4와 IFRS17의 손익인식 비교", "I-6 최선추정부채(BEL) 변동분석"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.2 보험수익 / 2.3 보험서비스비용 (제3장 손익계산서)"], "해설서 2.2 보험수익, 2.3 보험서비스비용, 제3장 전체가 이 절의 회계적 서술이다."),
    },
    {
        "num": "I-5", "title": "IFRS4와 IFRS17의 손익인식 비교", "page": 1180,
        "def": "IFRS4는 수입보험료를 수익으로, 지급보험금과 준비금 전입액을 비용으로 인식하는 현금주의에 가까운 방식이었다. IFRS17은 I-4의 산식으로 완전히 재구성된다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{IFRS4: 수익} = \text{수입보험료} \quad\quad \text{IFRS17: 수익} = I\text{-}4\text{의 산식}",
        "derivationSteps": [
            step("IFRS4에서는 계약자가 보험료를 낸 시점에 그 전액이 수익으로 잡히고, 이후 준비금 적립을 통해 비용으로 상쇄하는 구조였다.", None),
            step("IFRS17에서는 보험료 수취 자체는 수익이 아니며(부채의 증가일 뿐), I-4에서 정의한 '서비스 제공에 대응하는 몫'만 수익으로 인식한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 차이 때문에 IFRS17 도입 시 재무제표상 '보험수익'의 규모가 IFRS4의 '수입보험료'보다 훨씬 작아지는 경우가 많다 — 저축성 상품처럼 투자요소 비중이 큰 상품일수록 이 차이가 두드러진다.",
        "relatedFormulas": "I-4와의 대비.",
        "prerequisites": ["I-4 IFRS17 손익 인식"],
        "leadsTo": [],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.2 보험수익"]),
    },
    {
        "num": "I-6", "title": "최선추정부채(BEL) 변동분석", "titleEn": "BEL roll-forward", "page": 1182,
        "def": "기시 BEL에서 기말 BEL로 넘어가는 과정을 변동원인별로 쪼갠다. 6장 II-5의 계약자적립액 재귀식(ₜVx→ₜ₊₁Vx)을 IFRS17 회계처리 관점으로 완전히 재구성한 절이다.",
        "symbols": [sym("BEL₀", "기시 BEL"), sym("BEL₁", "기말 BEL")],
        "assumptions": [],
        "formula": r"BEL_1 = \underbrace{BEL_0(1+\delta)}_{\text{①이자부리}} + \underbrace{\Delta_{\text{비금융}}}_{\text{②비금융가정변동}} + \underbrace{\Delta_{\text{금융}}}_{\text{③금융가정변동}} - \underbrace{CF_{\text{실제}}}_{\text{④당기현금흐름}}",
        "derivationSteps": [
            step("6장 II-5의 재귀식 (ₜVx+P)(1+i)=qₓ₊ₜ·1+pₓ₊ₜ·ₜ₊₁Vx이 '기시값+보험료를 이자부리한 뒤 사건(사망)을 반영해 기말값을 얻는다'는 구조였음을 상기한다.", None),
            step("IFRS17 BEL 변동분석은 이 구조를 4가지 변동원인으로 명시적으로 분해한다 — ①이자부리(unwinding, 11장 I-8의 할인율 경과분), ②비금융가정 변동(9장 사망률·해지율 실적 vs 가정 차이), ③금융가정 변동(11장 I-9~10 할인율 변화), ④당기 실제 현금흐름(11장 II-2의 실제 CF).", None),
            step("네 요소를 결합하면 기말 BEL을 얻는다:", r"BEL_1 = BEL_0(1+\delta) + \Delta_{\text{비금융}} + \Delta_{\text{금융}} - CF_{\text{실제}}"),
        ],
        "derivation": "",
        "termMeanings": [term("①이자부리", "6장 II-7 미분방정식의 δV(t) 항에 대응"), term("②비금융가정변동", "실제 사망·해지 실적이 가정과 다를 때 발생하는 차이"), term("③금융가정변동", "결산시점 할인율이 이전과 달라졌을 때의 재평가 효과")],
        "intuition": "6장 II-7의 Thiele 미분방정식(V'(t)=δV(t)+P̄−(b(t)−V(t))μ(x+t))이 '이자부리+보험료−위험비용'이라는 3요소로 적립액 변화를 설명했다면, 이 절은 그 논리를 IFRS17 공시요건에 맞게 4가지 원인으로 재분류한 것이다.",
        "relatedFormulas": "6장 II-5·II-7의 완전한 재구성.",
        "prerequisites": ["6장 II-5 순보험료의 분해와 재귀식", "6장 II-7 계약자적립액과 미분방정식", "11장 II-3 BEL 산출식"],
        "leadsTo": ["I-7 위험조정(RA) 변동분석", "II-6 1차년도 BEL 변동분석"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.8 보험부채의 변동 (변동원인별 회계처리)"], "해설서 4.8의 변동원인별 분류(비금융가정변동/금융가정변동/보험료/사업비 등)와 표 구조까지 거의 동일하다."),
    },
    {
        "num": "I-7", "title": "위험조정(RA) 변동분석", "page": 1186,
        "def": "RA도 BEL과 유사한 롤포워드 구조를 갖되, '위험소멸(risk release)'이라는 고유한 변동요인이 추가된다.",
        "symbols": [sym("RA₀", "기시 RA"), sym("RA₁", "기말 RA")],
        "assumptions": [],
        "formula": r"RA_1 = RA_0(1+\delta) + \Delta_{\text{가정변동}} - \text{위험소멸분}",
        "derivationSteps": [
            step("I-6과 같은 이자부리·가정변동 원인이 RA에도 동일하게 적용된다.", None),
            step("추가로, 시간이 지나 보장기간이 줄어들수록 남은 불확실성(위험)이 줄어드는 만큼 RA도 소멸(release)되며, 이 소멸분이 그 기간 수익의 일부(I-4)로 인식된다.", r"RA_1 = RA_0(1+\delta)+\Delta_{\text{가정변동}} - \text{위험소멸분}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "RA는 '앞으로 남은 불확실성에 대한 대가'이므로, 보장기간이 지날수록(남은 불확실성이 줄어들수록) 자연스럽게 줄어드는 것이 당연하다 — 이 감소분이 바로 위험소멸분이다.",
        "relatedFormulas": "I-6과 같은 구조에 위험소멸 항목 추가.",
        "prerequisites": ["I-6 최선추정부채(BEL) 변동분석", "11장 I-3 책임준비금의 구성항목"],
        "leadsTo": ["I-8 보험계약마진(CSM) 변동분석"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.6.4 위험조정 변동원인별 회계처리"]),
    },
    {
        "num": "I-8", "title": "보험계약마진(CSM) 변동분석", "page": 1186,
        "def": "CSM 변동분석은 BEL·RA와 근본적으로 다른 논리를 따른다 — CSM은 '계약자에게 아직 제공하지 않은 미래서비스의 미실현이익'이므로, 미래서비스와 관련된 가정변경만 CSM을 조정하고, 과거·당기 서비스 관련 변경은 즉시 손익으로 인식된다는 것이 IFRS17 고유의 회계처리다.",
        "symbols": [sym("CSM₀", "기시 CSM"), sym("CSM₁", "기말 CSM")],
        "assumptions": [],
        "formula": r"CSM_1 = CSM_0(1+\delta) + \Delta_{\text{미래서비스 관련}} - \text{당기 상각액}",
        "derivationSteps": [
            step("CSM도 이자부리(①)를 거치지만, ②의 '비금융가정변동'은 BEL·RA와 달리 CSM에는 오직 '미래서비스와 관련된' 부분만 반영된다 — 이는 6장 I-2에서 강조했듯 CSM이 전통 보험수리학의 재귀식과 동일시될 수 없는 지점이다(BEL·RA의 재귀식은 순수하게 계리적 계산인 반면, CSM의 조정범위 판단은 IFRS17이 정한 회계정책적 구분이다).", None),
            step("마지막으로, 그 기간 제공한 서비스에 해당하는 몫만큼 CSM을 상각해 보험수익(I-4)으로 인식한다:", r"CSM_1 = CSM_0(1+\delta) + \Delta_{\text{미래서비스}} - \text{당기상각액}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "CSM 변동분석에서 가장 헷갈리는 부분이 바로 이 '미래서비스 관련 변경만 조정, 과거·당기 관련은 즉시 손익'이라는 구분이다. 이는 BEL·RA 변동분석(I-6, I-7)이 순수하게 계리 계산의 재귀식을 따르는 것과 달리, CSM은 '어느 기간에 귀속되는 변경인가'라는 회계적 판단이 추가로 개입한다는 점에서 근본적으로 다른 성격의 절차임을 분명히 해야 한다.",
        "relatedFormulas": "I-6, I-7과 형태는 유사하나 조정범위 판단이 근본적으로 다름.",
        "prerequisites": ["I-7 위험조정(RA) 변동분석", "6장 I-2 IFRS4 기준 책임준비금과 IFRS17 기준 책임준비금", "11장 I-2 IFRS17 책임준비금"],
        "leadsTo": ["I-9 보험부채의 변동과 손익 인식"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.7.3 보험계약마진의 조정 및 회계처리"], "해설서 4.7.3이 규정하는 CSM 조정항목(신규계약 추가, 이자부리, 미래서비스 관련 현금흐름 변동, 환율변동, 당기 상각액)의 순서를 그대로 따른다."),
    },
    {
        "num": "I-9", "title": "보험부채의 변동과 손익 인식", "page": 1189,
        "def": "BEL/RA/CSM 변동 중 어느 부분이 당기손익(보험손익), 어느 부분이 보험금융손익(P&L 또는 OCI)으로 가는지 매핑한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{보험손익} = (\text{서비스 관련 변동}) \qquad \text{보험금융손익} = (\text{이자부리+할인율변동})",
        "derivationSteps": [
            step("I-6~8에서 분해한 각 변동요인을 성격별로 재분류한다 — '보장 제공에 따른 변동'(사업 실적, 서비스 상각)은 보험손익으로, '화폐의 시간가치·금융위험에 따른 변동'(이자부리, 할인율변동)은 보험금융손익으로 구분된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 구분 원칙 덕분에 재무제표 이용자는 '보험 본연의 사업성과'와 '금융시장 변동에 따른 효과'를 분리해서 볼 수 있다 — IFRS4에서는 이 두 가지가 뒤섞여 있었다는 점이 6장 I-2에서 지적한 한계 중 하나다.",
        "relatedFormulas": "I-6~8의 재분류.",
        "prerequisites": ["I-8 보험계약마진(CSM) 변동분석"],
        "leadsTo": ["I-10 보험부채 변동분석과 손익인식의 구조분석"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.13 보험금융손익의 표시 및 인식"]),
    },
    {
        "num": "I-10", "title": "보험부채 변동분석과 손익인식의 구조분석", "page": 1190,
        "def": "I-6~9 전체를 하나의 종합 표로 정리 — II파트에서 실제 숫자로 이 표를 채워나가기 위한 최종 준비.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{(기시BEL, RA, CSM)} \xrightarrow{\text{변동요인}} \text{(기말BEL, RA, CSM)} \to \text{(보험손익, 보험금융손익)}",
        "derivationSteps": [
            step("I-6~9의 모든 관계식을 하나의 흐름도(기시값→변동요인 적용→기말값→손익 배분)로 통합 정리한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I파트 전체(기초이론)의 최종 요약이며, II파트(일반이론)에서 이 구조를 실제 상품·숫자로 완성한다.",
        "relatedFormulas": "I-6~9 전체의 통합.",
        "prerequisites": ["I-9 보험부채의 변동과 손익 인식"],
        "leadsTo": ["II-1 개요"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.8 보험부채의 변동"]),
    },
]

II = [
    {
        "num": "II-1", "title": "개요", "page": 1199,
        "def": "II파트에서 사용할 예시(3년만기 생사혼합보험)를 소개하고 전체 계산 순서를 개관한다.",
        "symbols": [],
        "assumptions": ["3년만기 생사혼합보험(3장 I-4) — 만기가 짧아 전체 과정을 한 번에 조망할 수 있음"],
        "formula": r"\text{0시점 최초측정} \to \text{1차년도 후속측정} \to \text{2차년도 후속측정}",
        "derivationSteps": [
            step("11장이 종신보험(긴 기간)을 예시로 택했다면, 12장은 짧은 만기(3년)의 상품을 택해 최초인식부터 만기까지 전 과정을 압축적으로 보여준다는 설계 의도를 밝힌다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "짧은 예시를 통해 I파트의 모든 이론(변동분석 4요소, 손익 배분)을 한 계약의 전체 생애주기에 걸쳐 확인할 수 있다.",
        "relatedFormulas": "3장 I-4 생사혼합보험의 재사용.",
        "prerequisites": ["I-10 보험부채 변동분석과 손익인식의 구조분석", "3장 I-4 생사혼합보험"],
        "leadsTo": ["II-2 금리확정형상품의 분석가정과 보험료산출"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "금리확정형상품의 분석가정과 보험료산출", "page": 1200,
        "def": "예시상품의 구체적 가정(예정이율, 예정사망률 등)과, 5장 이론에 따른 순보험료를 산출한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"P = \frac{A_{x:\overline{3}|}}{\ddot a_{x:\overline{3}|}} \quad (\text{5장 I-1의 재적용})",
        "derivationSteps": [
            step("5장 I-1의 수지상등원칙을, 3년만기 생사혼합보험(3장 I-4)에 그대로 적용해 순보험료를 계산한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "5장 이론이 실제 예시의 첫 단계(보험료 결정)에 그대로 쓰인다.",
        "relatedFormulas": "5장 I-1, 3장 I-4의 재적용.",
        "prerequisites": ["II-1 개요", "5장 I-1 연납평준순보험료"],
        "leadsTo": ["II-3 금리확정형상품의 보험부채 시가평가(0시점, 최초측정)"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-3", "title": "금리확정형상품의 보험부채 시가평가(0시점, 최초측정)", "page": 1203,
        "def": "계약 최초인식 시점(0시점)의 BEL·RA·CSM을 처음으로 산출하는, 이 책 전체 이론의 첫 실전 종합 사례.",
        "symbols": [],
        "assumptions": [],
        "formula": r"BEL_0 = PV(\text{유출}) - PV(\text{유입}), \quad CSM_0 = PV(\text{유입})-PV(\text{유출})-RA_0",
        "derivationSteps": [
            step("11장 II-3의 BEL 산출식을 이 3년 상품에 적용해 BEL₀을 구한다 — 이 때 사용하는 할인율·사망률·해지율은 5장의 예정기초율(가격산출용)이 아니라 최선추정 가정(11장 I-7)이다.", None),
            step("11장 I-3의 신뢰수준 방법으로 RA₀을 산출한다.", None),
            step("11장 I-3의 정의에 따라 CSM₀ = 유입현가 − 유출현가 − RA₀ (양수인 경우)로 최초 CSM을 확정한다.", r"CSM_0 = PV(\text{유입})-PV(\text{유출})-RA_0"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 절이 이 책 전체(1~11장)에서 배운 모든 도구가 실제로 하나의 계약에 처음 적용되는 순간이다.",
        "relatedFormulas": "11장 II-3, I-3의 실제 적용.",
        "prerequisites": ["II-2 금리확정형상품의 분석가정과 보험료산출", "11장 II-3 BEL 산출식", "11장 I-3 책임준비금의 구성항목"],
        "leadsTo": ["II-4 금리확정형상품의 보험부채 시가평가(k1시점, 후속측정)"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.7.2 보험계약마진의 최초인식", "제5장 회계사례 (회계처리 일반모형)"], "해설서 4.7.2(CSM 최초인식) 및 제5장 회계사례(최초인식 분개)와 정확히 대응된다."),
    },
    {
        "num": "II-4", "title": "금리확정형상품의 보험부채 시가평가(k1시점, 후속측정)", "page": 1217,
        "def": "1년 경과 후(1시점) 부채를 재평가하는 후속측정 — I-6~8의 변동분석 이론을 처음으로 실제 숫자에 적용한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"BEL_1, RA_1, CSM_1 \; (\text{I-6~8의 산식을 실제 숫자로 계산})",
        "derivationSteps": [
            step("1년 동안의 실제 사건(생존/사망/해지 실적)과 가정변경(있다면)을 반영해, I-6~8의 롤포워드 공식을 실제 숫자로 계산한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-3이 '최초인식'이라는 한 순간을 다뤘다면, 이 절부터는 시간이 흐르며 부채가 어떻게 갱신되는지(6장 재귀식의 진짜 실전 적용)를 보여준다.",
        "relatedFormulas": "I-6~8의 실제 적용.",
        "prerequisites": ["II-3 금리확정형상품의 보험부채 시가평가(0시점, 최초측정)", "I-6 최선추정부채(BEL) 변동분석"],
        "leadsTo": ["II-5 1차년도 BEL변동분석용 대와 BEL변동표"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.7.3 보험계약부채의 후속 측정"]),
    },
    {
        "num": "II-5", "title": "1차년도 BEL변동분석용 대와 BEL변동표", "page": 1224,
        "def": "I-6의 4가지 변동요인(이자부리, 비금융가정변동, 금융가정변동, 당기현금흐름)을 실제 숫자로 채운 변동분석표(BEL 변동표)를 작성한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"BEL_0 \to (+\text{이자부리}) \to (+\Delta_{\text{비금융}}) \to (+\Delta_{\text{금융}}) \to (-CF) \to BEL_1",
        "derivationSteps": [
            step("I-6의 산식을 항목별로 나눠 표(전형적으로 왼쪽에 항목명, 오른쪽에 금액을 나열하는 형태)로 정리한다 — 이는 해설서 4.8이 요구하는 공시 표 형식과 동일하다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "재무제표 주석에 실제로 공시되는 'BEL 조정내역' 표가 이런 형태로 만들어진다는 것을 보여주는 실무적 절이다.",
        "relatedFormulas": "I-6의 표 형태 구현.",
        "prerequisites": ["II-4 금리확정형상품의 보험부채 시가평가(k1시점, 후속측정)", "I-6 최선추정부채(BEL) 변동분석"],
        "leadsTo": ["II-6 1차년도 BEL 변동분석"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.8 보험부채의 변동"], "해설서 4.8이 요구하는 공시 형식(변동원인별 표)과 동일한 구조다."),
    },
    {
        "num": "II-6", "title": "1차년도 BEL 변동분석", "page": 1230,
        "def": "II-5의 표를 실제 숫자로 완전히 채워 BEL₀에서 BEL₁까지의 전 과정을 검증한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"BEL_1 = BEL_0(1+\delta) + \Delta_{\text{비금융}} + \Delta_{\text{금융}} - CF \; (\text{실제 값 대입, 검산})",
        "derivationSteps": [
            step("II-5에서 준비한 표의 각 항목에 실제 숫자를 대입하고, 합산 결과가 독립적으로 계산한 BEL₁(II-4)과 일치하는지 검증한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 검증(변동분석 합계 = 직접 계산한 기말값)이 일치해야 이론이 정합적으로 작동함을 확인할 수 있다 — 실무에서도 이런 대사(reconciliation)가 결산 검증의 핵심 절차다.",
        "relatedFormulas": "II-4, II-5의 검증.",
        "prerequisites": ["II-5 1차년도 BEL변동분석용 대와 BEL변동표"],
        "leadsTo": ["II-7 BEL(IB)과 BEL(FS)"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.8 보험부채의 변동"]),
    },
    {
        "num": "II-7", "title": "BEL(IB)과 BEL(FS)", "page": 1245,
        "def": "이행현금흐름 관점의 BEL(IB, Insurance Benefit 기준)과 재무제표 표시 관점의 BEL(FS, Financial Statement 기준) 사이의 표시상 차이를 다룬다.",
        "symbols": [sym("BEL(IB)", "이행현금흐름 계산 결과 그대로의 BEL"), sym("BEL(FS)", "재무제표에 실제 표시되는 BEL(발생사고요소 등과 구분)")],
        "assumptions": [],
        "formula": r"BEL(FS) = BEL(IB) \pm (\text{표시조정})",
        "derivationSteps": [
            step("계리적으로 계산된 BEL(IB)이, 재무상태표 표시 시 잔여보장요소/발생사고요소(11장 I-3, 해설서 5.1)로 구분 표시되면서 발생하는 조정을 다룬다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "계리적 계산과 회계적 표시가 개념적으로는 같은 것을 가리키지만, 실제 재무제표 양식에 맞추는 과정에서 세부 조정이 필요할 수 있음을 보여주는 실무적 절이다.",
        "relatedFormulas": "11장 I-3의 계정과목 구분.",
        "prerequisites": ["II-6 1차년도 BEL 변동분석", "11장 I-3 책임준비금의 구성항목"],
        "leadsTo": ["II-8 1차년도 보험계약마진(CSM) 변동분석"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 5.1 잔여보장요소 (보험부채 계정과목별 해설)"]),
    },
    {
        "num": "II-8", "title": "1차년도 보험계약마진(CSM) 변동분석", "page": 1248,
        "def": "I-8의 CSM 변동분석을 실제 숫자로 완결한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"CSM_1 = CSM_0(1+\delta) - \text{당기상각액} \; (\text{가정변경 없다고 가정한 단순 사례})",
        "derivationSteps": [
            step("I-8의 산식에 실제 숫자를 대입해 1차년도 CSM 상각액과 기말 CSM을 산출한다.", None),
            step("이 상각액이 II-9의 손익계산서에서 보험수익의 핵심 구성요소(I-4)로 나타난다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-8에서 이론적으로 강조했던 '미래서비스 관련 변경만 CSM 조정'이라는 원칙이 실제로 어떻게 적용되는지 이 예시에서 확인할 수 있다.",
        "relatedFormulas": "I-8의 실제 적용.",
        "prerequisites": ["II-7 BEL(IB)과 BEL(FS)", "I-8 보험계약마진(CSM) 변동분석"],
        "leadsTo": ["II-9 1차년도 재무제표"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.7.3 보험계약마진의 조정 및 회계처리"]),
    },
    {
        "num": "II-9", "title": "1차년도 재무제표", "page": 1251,
        "def": "II-6~8에서 산출한 BEL·RA·CSM 변동을 실제 재무상태표·손익계산서 양식으로 완성한다 — 이 책 전체 이론이 최종적으로 도달하는 산출물.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{재무상태표: 보험계약부채} = BEL_1+RA_1+CSM_1 \qquad \text{손익계산서: 보험수익(I-4)} - \text{보험서비스비용}",
        "derivationSteps": [
            step("재무상태표에는 기말 부채(BEL₁+RA₁+CSM₁)가 표시된다.", None),
            step("손익계산서에는 I-4의 보험수익 산식과, 실제 발생한 보험서비스비용(발생보험금 등)이 표시되어 보험손익이 확정된다.", None),
            step("I-9에서 정리한 보험손익·보험금융손익 구분에 따라 각 항목이 배분된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "1장의 이자론부터 시작한 이 책의 모든 이론이, 결국 이 재무제표 두 장(재무상태표·손익계산서)을 만들어내기 위한 것이었다는 점에서 이 절이 사실상 전체 이론의 종착점이다.",
        "relatedFormulas": "I-4, I-9 전체의 최종 구현.",
        "prerequisites": ["II-8 1차년도 보험계약마진(CSM) 변동분석", "I-9 보험부채의 변동과 손익 인식"],
        "leadsTo": ["II-10 2차년도 변동분석"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["제5장 회계사례 (재무제표 양식)"], "해설서 제5장 회계사례와 나란히 놓고 보면 가장 이해가 빠른 조합이다 — 12장이 '계리적으로 숫자를 어떻게 산출하는가'를, 해설서 5장이 '그 숫자를 회계상 어떤 분개로 기록하는가'를 보여준다."),
    },
    {
        "num": "II-10", "title": "2차년도 변동분석", "page": 1258,
        "def": "II-4~9의 전 과정을 2차년도에 대해 반복해, 이 순환 구조가 만기까지 계속됨을 확인한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"BEL_1,RA_1,CSM_1 \xrightarrow{\text{II-4~9와 동일한 절차}} BEL_2,RA_2,CSM_2 \to \text{2차년도 재무제표}",
        "derivationSteps": [
            step("1차년도 기말값(BEL₁, RA₁, CSM₁)을 2차년도의 기시값으로 놓고, II-4~9와 완전히 동일한 절차(변동분석→재무제표)를 반복한다.", None),
            step("이 순환이 3년만기 상품이므로 만기(3차년도)까지 반복되면, 계약 전 생애주기의 회계처리가 완성된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "6장 II-5의 재귀식이 '한 스텝'의 논리였다면, 12장 전체는 그 한 스텝을 계약 만기까지 반복 적용하는 것이 IFRS17 후속측정의 본질임을 보여준다. 이것으로 최신보험수리학 전체 이론(1~12장)이 완결된다.",
        "relatedFormulas": "II-4~9 전체의 반복.",
        "prerequisites": ["II-9 1차년도 재무제표"],
        "leadsTo": [],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.7 보험부채 변동 회계처리"], "이 반복 구조 자체가 해설서 2.7이 규정하는 '보험계약부채의 후속 측정'의 매 결산기 반복 절차와 정확히 같다."),
    },
]

data_ch12 = {
    "num": 12, "title": "보험부채 변동분석과 손익인식",
    "summary": "11장에서 평가한 보험부채가 기간 경과에 따라 어떻게 변동하고, 그 변동이 어떻게 손익(보험손익/보험금융손익)으로 인식되는지를 다루는 장. I-6~8(BEL·RA·CSM 변동분석)이 6장의 계약자적립액 재귀식을 IFRS17 회계처리로 완전히 재구성하며, II파트의 3년만기 예시가 이 책 전체 이론의 최종 종합이다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 12:
        data["chapters"][i] = data_ch12
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 12 upgraded:", len(I) + len(II), "items")
