# -*- coding: utf-8 -*-
# 제11장 보험부채 시가평가 — 12-field schema. IFRS17과 가장 직접 연결되는 핵심 장이라 최대한 신중하게 작성.
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
        "num": "I-1", "title": "보험부채 시가평가 개요", "page": 1060,
        "def": "11장·12장 전체가 다루는 '보험부채 시가평가'라는 과제를 개관한다. 장래현금흐름을 생성하려면 6장의 계약자적립액·9장의 월별 다중탈퇴율·1장의 월별 할인율 시나리오를 종합적으로 이해해야 한다는, 이 책 전체 이론이 수렴하는 지점임을 밝힌다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{보험부채 시가평가} = f(\text{계약자적립액}, \text{월별 다중탈퇴율}, \text{월별 할인율 시나리오})",
        "derivationSteps": [
            step("11장은 장래현금흐름 모형(부채 최초 시가평가)을, 12장은 그 부채의 변동분석(후속측정)을 다룬다는 두 장의 역할 분담을 제시한다.", None),
            step("11장 기초이론에서는 ①IFRS17 책임준비금 구성(BEL/RA/CSM), ②월별 다중탈퇴율(9장의 확장), ③할인율 산출(1장의 확장)이라는 세 축을 순서대로 다룬다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 장은 완전히 새로운 이론이 아니라, 1~10장에서 개별적으로 배운 도구들(할인, 생존확률, 다중탈퇴, 계약자적립액)을 '월 단위'로 재조립해 IFRS17이라는 새로운 목적에 맞게 통합하는 장이다.",
        "relatedFormulas": "1장(할인), 6장(적립액), 9장(다중탈퇴)의 통합.",
        "prerequisites": ["6장 I-1 책임준비금의 산출(평가)방법", "9장 II-5 다중탈퇴율의 계산", "1장 I-5 이력과 할인력"],
        "leadsTo": ["I-2 IFRS17 책임준비금"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.1~4.13 보험부채 총론 전체"], "이 장 전체가 해설서 제2장 제4절(보험부채 총론)을 계리적으로 구현한 것이다."),
    },
    {
        "num": "I-2", "title": "IFRS17 책임준비금", "page": 1061,
        "def": "IFRS17 보험계약부채 = 이행현금흐름(최선추정부채 BEL + 위험조정 RA) + 보험계약마진(CSM). 6장 I-2에서 개관했던 이 구조를 여기서 본격적으로 계리 계산 대상으로 삼는다.",
        "symbols": [sym("BEL", "최선추정부채(Best Estimate Liability)"), sym("RA", "위험조정(Risk Adjustment)"), sym("CSM", "보험계약마진(Contractual Service Margin)")],
        "assumptions": [],
        "formula": r"\text{보험계약부채} = BEL + RA + CSM",
        "derivationSteps": [
            step("BEL은 미래현금흐름을 최선추정 가정으로 현재가치화한 기대값이다(11장 II에서 구체적으로 산출).", None),
            step("RA는 비금융위험의 불확실성을 부담하는 대가로 더해지는 완충금이다(5장의 백분위 보험료·7장 II-3의 Var(L)과 통계적으로 같은 발상).", None),
            step("CSM은 최초인식 시점 '유입현금흐름 현가 − 유출현금흐름 현가 − RA'가 양(+)일 때 그 초과분을 이연한 것이다. 이 CSM은 전통 보험수리학 공식으로 환원되지 않는 IFRS17 고유의 회계개념이라는 점을 6장 I-2에서 강조했다 — 여기서도 CSM 산출에 필요한 '재료'(BEL, RA)는 계리적으로 계산하지만, CSM 자체의 이연·상각 메커니즘은 회계처리임을 구분해야 한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "6장 I-2가 '개념 소개'였다면 이 절부터는 '실제로 어떻게 계산하는가'로 넘어간다.",
        "relatedFormulas": "6장 I-2의 재확인.",
        "prerequisites": ["6장 I-2 IFRS4 기준 책임준비금과 IFRS17 기준 책임준비금"],
        "leadsTo": ["I-3 책임준비금의 구성항목"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.5 위험조정 / 2.6 보험계약마진 (총론)", "IFRS17 4.6 위험조정 / 4.7 보험계약마진 (부채총론)"], "해설서 2.6/4.7의 CSM 정의, 2.5/4.6의 RA 정의와 그대로 대응하는 개념 정의부다."),
    },
    {
        "num": "I-3", "title": "책임준비금의 구성항목", "page": 1063,
        "def": "BEL·RA·CSM 세 요소를 각각 어떻게 산출하는지 더 상세히 분해한다.",
        "symbols": [sym("BEL", "미래 유출현금흐름 현가 − 미래 유입현금흐름 현가"), sym("RA", "신뢰수준 기준 완충금")],
        "assumptions": [],
        "formula": r"BEL = PV(\text{유출}) - PV(\text{유입}), \qquad CSM_0 = \max\big(PV(\text{유입})-PV(\text{유출})-RA,\; 0\big)",
        "derivationSteps": [
            step("BEL은 유입현금흐름(보험료)과 유출현금흐름(보험금·해지환급금·사업비)의 현재가치 차액으로 정의된다 — 3~9장에서 다룬 모든 APV 계산이 이 유출·유입 항목의 재료가 된다.", None),
            step("RA는 신뢰수준(예: 75% CTE 등) 기준으로 산출되며, 이는 7장 II-5(백분위 보험료)의 신뢰수준 논리와 통계적으로 동일한 아이디어다.", None),
            step("CSM은 최초인식시점 '유입현가−유출현가−RA'가 양(+)일 때 그 초과분으로 설정된다. 음수이면 CSM은 0이 되고 그 부족분은 즉시 손실로 인식된다(손실계약):", r"CSM_0 = \max\big(PV(\text{유입})-PV(\text{유출})-RA,\;0\big)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 세 요소는 실무적으로 재무상태표의 실제 계정과목으로 나타나며, IFRS17 해설서가 '잔여보장요소(BEL+RA+CSM)'라는 이름으로 규정하는 부분과 정확히 대응된다.",
        "relatedFormulas": "3~9장의 모든 APV 계산이 BEL 산출의 재료.",
        "prerequisites": ["I-2 IFRS17 책임준비금"],
        "leadsTo": ["I-4 IFRS4와 IFRS17의 보험부채 비교", "II-3 BEL 산출식"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 5.1 잔여보장요소 (보험부채 계정과목별 해설)"], "BEL·RA·CSM 분해가 해설서 5.1 '잔여보장요소(최선추정부채/위험조정/보험계약마진)' 계정과목 해설과 그대로 짝지어진다."),
    },
    {
        "num": "I-4", "title": "IFRS4와 IFRS17의 보험부채 비교", "page": 1066,
        "def": "6장 I-2의 비교를 부채 시가평가 관점에서 재확인한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{IFRS4: 고정 예정기초율} \quad \text{vs} \quad \text{IFRS17: 매결산시점 최선추정 재계산}",
        "derivationSteps": [
            step("IFRS4는 계약시점 기초율을 고정해 부채가 시장금리 변화와 무관하게 움직인다.", None),
            step("IFRS17은 매 결산시점 할인율·사망률·해지율을 다시 추정해 부채를 재평가하므로, 시장금리·계리가정 변화가 즉시 부채와 손익에 반영된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "6장 I-2와 짝을 이루는 비교로, 이번에는 '부채가 시장 변화에 얼마나 민감하게 반응하는가'라는 관점에서 재확인한다.",
        "relatedFormulas": "6장 I-2의 재확인.",
        "prerequisites": ["6장 I-2 IFRS4 기준 책임준비금과 IFRS17 기준 책임준비금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.7.3 보험계약부채의 후속 측정"], "6장 I-2와 동일한 근거."),
    },
    {
        "num": "I-5", "title": "월별 다중탈퇴율 산출 개요", "page": 1067,
        "def": "9장의 연 단위 다중탈퇴모형을 월 단위로 세분화해야 하는 이유와 전체 절차를 개관한다. IFRS17 부채는 월별로 현금흐름을 인식하므로, 연 단위 기초율을 월 단위로 정교하게 쪼개는 절차가 필요하다.",
        "symbols": [],
        "assumptions": ["2장 II-9의 단수부분 가정(UDD 등)을 월 단위로 적용"],
        "formula": r"q^{(j)}_{x,\,\text{월}} \leftarrow q^{(j)}_x \; (\text{연간 다중탈퇴율을 월 단위로 세분화})",
        "derivationSteps": [
            step("2장 II-9의 단수부분 가정(UDD)을 이용하면, 연간 사망확률 qₓ를 그 해 안의 임의 시점(s)까지의 사망확률 ₛqₓ=s·qₓ로 나눌 수 있었다.", None),
            step("이 원리를 9장의 다중탈퇴확률 q⁽ʲ⁾ₓ에 그대로 적용해, 12개월 각각에 대한 월별 다중탈퇴율을 산출한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "2장의 단수부분 가정과 9장의 다중탈퇴모형이 결합되어야 이 절차가 가능하다는 점에서, 이 절이야말로 앞선 여러 장의 결합점이다.",
        "relatedFormulas": "2장 II-9, 9장 I-2의 결합.",
        "prerequisites": ["2장 II-9 단수부분에 대한 가정", "9장 I-2 다중탈퇴 확률"],
        "leadsTo": ["I-6 보험료산출 및 적립액산출 목적의 다중탈퇴율"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4.5 미래현금흐름의 예측방법"], "해설서가 요구하는 미래현금흐름 추정을 월 단위로 정밀하게 수행하기 위한 계리적 준비 작업이다."),
    },
    {
        "num": "I-6", "title": "보험료산출 및 적립액산출 목적의 다중탈퇴율", "page": 1068,
        "def": "같은 계약이라도 '가격산출(보험료 결정) 목적'으로는 상품 개발 시점에 정한 예정기초율을 사용한다는 점을 정리한다.",
        "symbols": [],
        "assumptions": ["7장 I-3의 현금흐름방식 보험료산출 시점 기준 최선추정 가정"],
        "formula": r"q^{(j)}_{x,\,\text{가격산출용}} = (\text{상품개발 시점에 고정된 기초율})",
        "derivationSteps": [
            step("7장 I-3에서 다룬 현금흐름방식 보험료산출은 상품 출시 시점에 '그 당시의 최선추정'으로 기초율을 고정한다 — 이후 실제 경험이 달라져도 이미 판매된 상품의 보험료 자체는 바뀌지 않는다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이는 6장 I-4~5(순보식 계약자적립액)에서 쓰는 기초율과 같은 성격 — '한 번 정하면 그 계약에서는 계속 쓰는' 기초율이다.",
        "relatedFormulas": "7장 I-3, 6장 I-5의 재확인.",
        "prerequisites": ["7장 I-3 현금흐름방식의 보험료산출", "6장 I-5 금리확정형상품의 장래법 계약자적립액의 산출"],
        "leadsTo": ["I-7 부채평가 목적의 다중탈퇴율"],
        "ifrs17": ifrs("간접적 연관", note="가격산출용 기초율 자체는 IFRS17 부채평가와 직접 관련되지 않지만, I-7과의 대비를 위한 배경 설명이다."),
    },
    {
        "num": "I-7", "title": "부채평가 목적의 다중탈퇴율", "page": 1070,
        "def": "부채평가 목적으로는 결산시점의 최선추정 기초율(9장 II-4의 절대탈퇴율 개념을 회사 고유 경험통계로 매번 재추정)을 사용한다는 점을 대비시킨다. 이 절이 9장 II-4(절대탈퇴율 vs 다중탈퇴율)의 직접적인 실무 적용이다.",
        "symbols": [sym("q'⁽ʲ⁾ₓ,결산시점", "그 결산시점의 최신 경험통계로 추정한 절대탈퇴율")],
        "assumptions": ["매 결산시점마다 최신 경험통계로 재추정(9장 II-4~5의 절차 반복)"],
        "formula": r"q^{(j)}_{x,\,\text{부채평가용}} = (\text{그 결산시점의 최선추정 기초율}) \ne q^{(j)}_{x,\,\text{가격산출용}}",
        "derivationSteps": [
            step("I-6의 가격산출용 기초율과 달리, 부채평가용 기초율은 매 결산시점마다 그때까지의 최신 경험통계를 반영해 다시 추정한다.", None),
            step("이 재추정 절차는 9장 II-4~5에서 다룬 '절대탈퇴율로부터 다중탈퇴율 산출' 과정을 결산시점마다 반복하는 것과 같다 — 다만 이번에는 상품개발 시점이 아니라 매 결산시점이 기준이라는 점이 다르다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-6·I-7의 대비가 이 장에서 가장 중요한 개념적 포인트다 — '같은 계약, 다른 두 종류의 기초율'이라는 구조가 바로 IFRS4(고정 가정, I-6과 유사)와 IFRS17(매번 재평가, I-7)의 근본적 차이(I-4)를 계리적으로 실현하는 지점이다.",
        "relatedFormulas": "9장 II-4~5의 실무 적용. I-6과의 대비.",
        "prerequisites": ["9장 II-4 절대탈퇴율의 계산", "9장 II-5 다중탈퇴율의 계산", "I-6 보험료산출 및 적립액산출 목적의 다중탈퇴율"],
        "leadsTo": ["I-8 IFRS17 기준과 감독규정상의 할인율 산출방법"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4.5 미래현금흐름의 예측방법"], "해설서 4.4.5가 요구하는 '회사 고유의 경험통계를 반영한 최선추정' 원칙을 계리적으로 완전히 구현하는 절이다."),
    },
    {
        "num": "I-8", "title": "IFRS17 기준과 감독규정상의 할인율 산출방법", "page": 1078,
        "def": "1장 I-5(이력)의 실무 구현으로, 무위험수익률에 유동성프리미엄을 더한 '조정무위험금리기간구조'를 산출하는 방법.",
        "symbols": [sym("rf(t)", "만기 t의 무위험수익률"), sym("LP", "유동성프리미엄(liquidity premium)"), sym("δ(t)", "조정된 할인율(기간별)")],
        "assumptions": ["할인율이 만기별로 다른 기간구조(term structure)를 가짐(1장 I-2의 iₙ이 매기 달라질 수 있다는 논리의 실무 확장)"],
        "formula": r"\delta(t) = r_f(t) + LP(t)",
        "derivationSteps": [
            step("1장 I-5의 이력 δ는 원래 모든 만기에 동일한 상수였지만, 실무에서는 만기별로 다른 무위험수익률 rf(t)를 사용한다(1장 I-2에서 iₙ이 매기 달라질 수 있음을 이미 다뤘다).", None),
            step("여기에 보험부채 현금흐름의 유동성 특성을 반영한 유동성프리미엄 LP(t)를 더해 조정한다:", r"\delta(t) = r_f(t)+LP(t)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "1장이 '단일 이자율로 할인'을 다뤘다면, 이 절은 '만기별로 다른 이자율(기간구조)'로 확장한 것이다.",
        "relatedFormulas": "1장 I-2, I-5의 확장.",
        "prerequisites": ["1장 I-2 단리와 복리(실이율)", "1장 I-5 이력과 할인력"],
        "leadsTo": ["I-9 결정론적 할인율 시나리오"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.5 할인율"], "해설서 4.5의 '무위험수익률+유동성프리미엄'을 반영한 조정무위험금리기간구조 산출법과 정확히 대응된다."),
    },
    {
        "num": "I-9", "title": "결정론적 할인율 시나리오", "titleEn": "deterministic scenario", "page": 1079,
        "def": "단일 금리경로(하나의 확정된 미래 금리 예측)를 가정해 부채를 평가하는 방식.",
        "symbols": [],
        "assumptions": ["미래 금리가 하나의 경로로 확정된다고 가정(옵션·보증이 없는 단순한 상품에 적합)"],
        "formula": r"BEL = \sum_t CF_t \cdot \prod_{s\le t}(1+\delta(s))^{-1}",
        "derivationSteps": [
            step("I-8에서 구한 기간별 할인율 δ(t)를 하나의 확정 경로로 사용해, 각 시점의 현금흐름을 순차적으로 할인해 합산한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "옵션·보증이 없는 단순한 금리확정형상품이라면, 미래 금리 경로가 어떻든 부채 계산 결과가 크게 달라지지 않으므로 이 단순한 방법으로 충분하다.",
        "relatedFormulas": "I-8의 직접 적용.",
        "prerequisites": ["I-8 IFRS17 기준과 감독규정상의 할인율 산출방법"],
        "leadsTo": ["I-10 확률론적 할인율 시나리오"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.5.4 할인율 변동에 대한 회계처리"], "해설서가 규정하는 할인율 적용 방법의 실무 절차와 대응된다."),
    },
    {
        "num": "I-10", "title": "확률론적 할인율 시나리오", "titleEn": "stochastic scenario", "page": 1083,
        "def": "여러 금리경로를 확률적으로 생성(이자율모형 시뮬레이션)해, 옵션·보증이 포함된 금리연동형상품의 부채를 평가하는 방식.",
        "symbols": [sym("N", "생성하는 시나리오 개수"), sym("BELⁿ", "n번째 시나리오에서의 BEL")],
        "assumptions": ["금리연동형상품처럼 옵션·보증(예: 최저보증이율)이 있어 부채가 금리경로에 비선형적으로 반응하는 경우"],
        "formula": r"BEL = \frac{1}{N}\sum_{n=1}^N BEL^n(\text{시나리오}_n)",
        "derivationSteps": [
            step("옵션·보증이 있는 상품은 '금리가 오를 때'와 '내릴 때'의 부채 반응이 비대칭적이므로(예: 최저보증이율 하한 때문에 금리 하락시에만 보증이 발동), 단일 결정론적 경로(I-9)로는 이 비대칭성을 포착할 수 없다.", None),
            step("여러 개의 확률적 금리경로(시나리오)를 생성해 각각에서 BEL을 계산한 뒤, 그 평균을 최종 BEL로 사용한다(몬테카를로 방식):", r"BEL = \frac{1}{N}\sum_n BEL^n"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이것이 결정론적(I-9)과 확률론적(I-10) 방법의 핵심 차이다 — 부채가 금리에 선형적으로 반응하면 단일 경로로 충분하지만, 옵션성(비선형성)이 있으면 여러 시나리오의 평균을 내야 정확한 기대값을 얻을 수 있다(옌센의 부등식과 관련된 논리).",
        "relatedFormulas": "I-9와의 대비.",
        "prerequisites": ["I-9 결정론적 할인율 시나리오"],
        "leadsTo": ["II-1 보험부채 평가모형 개요"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.9 변동수수료모형"], "옵션·보증이 있는 상품(변동수수료모형 VFA 적용 대상)의 정확한 부채평가에는 이 확률론적 시나리오가 실무적으로 요구된다."),
    },
]

II = [
    {
        "num": "II-1", "title": "보험부채 평가모형 개요", "page": 1096,
        "def": "I파트의 개념들을 실제 산출식으로 옮기기 위한 기호체계를 정의한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{장래현금흐름 모형: 계약자적립액} + \text{다중탈퇴율} + \text{할인율 시나리오} \to BEL",
        "derivationSteps": [
            step("II-2~4에서 사용할 장래현금흐름·BEL 산출식의 기호를 미리 정의하고, I파트에서 다룬 세 요소(계약자적립액, 다중탈퇴율, 할인율)를 조합하는 전체 흐름을 개관한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이제부터는 이론이 아니라 실제 숫자를 다루는 계산 절차로 넘어간다.",
        "relatedFormulas": "I파트 전체의 통합.",
        "prerequisites": ["I-10 확률론적 할인율 시나리오"],
        "leadsTo": ["II-2 장래현금흐름 모형"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"]),
    },
    {
        "num": "II-2", "title": "장래현금흐름 모형", "page": 1098,
        "def": "매월 발생하는 유지자·사망자·해지자수와 각각의 현금흐름을 정의하는 상세 기호체계.",
        "symbols": [sym("lₓ₊ₖ/₁₂⁽τ⁾", "k개월 경과시점 유지자수"), sym("CFₖ", "k개월째 순현금흐름(유입−유출)")],
        "assumptions": ["월 단위 다중탈퇴율(I-5) 사용"],
        "formula": r"CF_k = (\text{보험료 수입}_k) - (\text{보험금+해지환급금+사업비 지출}_k)",
        "derivationSteps": [
            step("I-5~7에서 산출한 월별 다중탈퇴율을 이용해, 매월 몇 명이 유지·사망·해지하는지를 순차적으로 계산한다(9장 I-1의 다중탈퇴표를 월 단위로 재구성).", None),
            step("각 월의 순현금흐름은 그 달의 보험료 수입에서 보험금·해지환급금·사업비 지출을 뺀 값이다.", r"CF_k = (\text{보험료수입}_k) - (\text{보험금+해지환급금+사업비}_k)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "9장의 다중탈퇴표를 월 단위, 실제 금액 단위로 완전히 구체화한 것이 이 모형이다.",
        "relatedFormulas": "9장 I-1, I-5의 월 단위·금액 단위 구체화.",
        "prerequisites": ["II-1 보험부채 평가모형 개요", "9장 I-1 다중탈퇴잔존표(다중탈퇴표)"],
        "leadsTo": ["II-3 BEL 산출식"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "해설서 4.4가 요구하는 미래현금흐름 항목(보험료, 보험금, 해지환급금, 사업비)을 월 단위로 완전히 구현한다."),
    },
    {
        "num": "II-3", "title": "BEL 산출식", "page": 1102,
        "def": "II-2의 월별 현금흐름을 I-8~10의 할인율로 현재가치화해 BEL을 산출하는 최종 산식. 이 책 전체 이론이 하나의 식으로 응축되는 지점이다.",
        "symbols": [sym("BEL₀", "0시점(평가시점) 기준 BEL"), sym("v(k)", "k개월 시점까지의 누적 할인계수(I-8의 δ(t) 기반)")],
        "assumptions": [],
        "formula": r"BEL_0 = \sum_{k=1}^{n} CF_k \cdot v(k) \cdot \frac{l^{(\tau)}_{k}}{l^{(\tau)}_0}",
        "derivationSteps": [
            step("3장 I-1의 APV 정의(현가×확률의 합)를 이 월별 모형에 다시 적용한다 — 각 월의 순현금흐름 CFₖ에, 그 시점까지 계약이 유지되어 있을 확률(lₖ⁽τ⁾/l₀⁽τ⁾, 9장)과 할인계수 v(k)(I-8)를 곱해 전 계약기간에 대해 합산한다.", r"BEL_0 = \sum_{k=1}^n CF_k\cdot v(k)\cdot \frac{l^{(\tau)}_k}{l^{(\tau)}_0}"),
        ],
        "derivation": "",
        "termMeanings": [term("CFₖ", "II-2에서 정의한 그 달의 순현금흐름"), term("v(k)", "I-8~10에서 산출한 그 시점까지의 할인계수"), term("lₖ⁽τ⁾/l₀⁽τ⁾", "9장의 다중탈퇴표에서 구한, 그 시점까지 계약이 유지될 확률")],
        "intuition": "이 식이 사실상 이 책 1~11장 전체가 만나는 지점이다 — 1장(할인 v(k)), 2·9장(생존·탈퇴확률), 3~7장(현금흐름 CFₖ의 구성원리)이 모두 이 한 줄의 공식 안에 녹아 있다.",
        "relatedFormulas": "3장 I-1 APV 정의의 최종 확장판.",
        "prerequisites": ["II-2 장래현금흐름 모형", "I-8 IFRS17 기준과 감독규정상의 할인율 산출방법", "3장 I-1 보험료계산의 기초"],
        "leadsTo": ["II-4 장래현금 구성항목과 장래현금흐름"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름 (미래현금흐름의 특성과 포함항목)"], "해설서 4.4를 수식으로 완전히 옮긴 것이 이 BEL 산출식이다."),
    },
    {
        "num": "II-4", "title": "장래현금 구성항목과 장래현금흐름", "page": 1105,
        "def": "II-2의 CFₖ를 실제 보험상품의 구체적 항목(위험보험료, 해약환급금, 사업비 등)으로 세분화한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"CF_k = P_k - (\text{사망보험금}_k + \text{해지환급금}_k + \text{사업비}_k)",
        "derivationSteps": [
            step("II-2의 일반식을 실제 보험 실무의 항목명으로 구체화한다.", r"CF_k = P_k - (\text{사망보험금}_k+\text{해지환급금}_k+\text{사업비}_k)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-3의 산식이 이론이라면, 이 절은 그 재료를 실무 계정과목 단위로 준비하는 절차다.",
        "relatedFormulas": "II-2, II-3의 세분화.",
        "prerequisites": ["II-2 장래현금흐름 모형"],
        "leadsTo": ["II-6 장래현금흐름 산출 가정"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4.1 미래현금흐름의 특성과 포함항목"]),
    },
    {
        "num": "II-5", "title": "금리연동형 UL종신보험의 개요", "page": 1109,
        "def": "이후 예시로 사용할 구체적 상품(유니버셜라이프 종신보험)의 급부구조를 소개한다.",
        "symbols": [sym("AVₖ", "k개월 시점 계약자적립액(6장 I-6의 월 단위 버전)")],
        "assumptions": ["매월 공시이율로 부리, 보너스적립액 등 추가 기능 존재"],
        "formula": r"AV_k = AV_{k-1}(1+i_k^{(12)}) + P_k - (\text{위험보험료+사업비})_k",
        "derivationSteps": [
            step("6장 I-6의 연 단위 갱신식을 월 단위로 세분화한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-8·II-9의 구체적 계산 예시를 위한 상품 소개 절이다.",
        "relatedFormulas": "6장 I-6의 월 단위 버전.",
        "prerequisites": ["6장 I-6 금리연동형보험의 계약자적립액"],
        "leadsTo": ["II-9 금리연동형상품의 사망보험금과 보너스적립액"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-6", "title": "장래현금흐름 산출 가정", "page": 1113,
        "def": "예시 계산에 사용할 구체적 가정(사망률, 해지율, 사업비율, 할인율 등)을 명시한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{(예시 계산을 위한 구체적 가정값 명시)}",
        "derivationSteps": [
            step("II-8~10의 실제 숫자 계산을 위해 필요한 모든 가정(9장의 다중탈퇴율, I-8~10의 할인율 등)을 표로 정리한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이론과 예시 계산을 잇는 실무적 준비 단계다.",
        "relatedFormulas": "I-5~10 전체의 구체화.",
        "prerequisites": ["II-4 장래현금 구성항목과 장래현금흐름"],
        "leadsTo": ["II-7 보험부채 시가평가 가정과 분석상품"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-7", "title": "보험부채 시가평가 가정과 분석상품", "page": 1116,
        "def": "II-8(금리확정형)과 II-9~10(금리연동형)에서 각각 사용할 분석상품(종신보험)의 구체적 스펙을 확정한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{(분석상품 스펙: 보험기간, 보험금액, 보험료 등)}",
        "derivationSteps": [
            step("보험기간이 최장인 종신보험을 선택해 긴 기간의 장래현금흐름의 큰 그림을 보여주고 분석하고자 한다는 저자의 설계 의도를 명시한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "종신보험을 예시로 택한 이유는, 만기가 있는 상품보다 훨씬 긴 시계열의 현금흐름을 다루므로 이 장의 모든 이론(할인·다중탈퇴·적립액)이 충분히 드러나기 때문이다.",
        "relatedFormulas": "II-6의 구체화.",
        "prerequisites": ["II-6 장래현금흐름 산출 가정"],
        "leadsTo": ["II-8 금리확정형상품의 보험부채 시가평가"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-8", "title": "금리확정형상품의 보험부채 시가평가", "page": 1120,
        "def": "II-3의 BEL 산출식을 실제 금리확정형 종신보험에 처음부터 끝까지 적용하는 완결된 예시.",
        "symbols": [],
        "assumptions": ["예정이율 고정(6장 I-5와 같은 상품이지만 부채평가는 최선추정 할인율로 별도 수행)"],
        "formula": r"BEL_0 = \sum_{k=1}^{n} CF_k\cdot v(k)\cdot \frac{l^{(\tau)}_k}{l^{(\tau)}_0} \quad (\text{실제 숫자 대입})",
        "derivationSteps": [
            step("II-4에서 정의한 CFₖ(보험료−사망보험금−해지환급금−사업비)를 매월 계산한다.", None),
            step("9장의 다중탈퇴표(사망·해지)로 매월 유지자수를 갱신한다.", None),
            step("I-8~9의 할인율로 각 월의 CFₖ를 현재가치화해 II-3의 산식대로 합산하면 BEL₀을 얻는다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-3의 이론적 산식을 실제 상품에 적용한 첫 완결 사례로, 해설서의 서술적 설명(4.1~4.11)을 숫자로 구현한 버전이라고 보면 가장 이해가 빠르다.",
        "relatedFormulas": "II-3의 실제 적용.",
        "prerequisites": ["II-3 BEL 산출식", "II-7 보험부채 시가평가 가정과 분석상품"],
        "leadsTo": ["II-9 금리연동형상품의 사망보험금과 보너스적립액"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.8 보험부채의 변동"], "이 예시가 해설서 4.1~4.11(보험부채 총론)의 서술 내용을 실제 숫자로 완전히 구현한다."),
    },
    {
        "num": "II-9", "title": "금리연동형상품의 사망보험금과 보너스적립액", "page": 1132,
        "def": "II-5의 UL종신보험처럼 적립액 연동형 사망보험금과, 공시이율이 최저보증이율을 초과할 때 추가되는 보너스적립액을 다룬다.",
        "symbols": [sym("보너스적립액", "공시이율이 예정이율(또는 최저보증)을 초과하는 부분에서 발생하는 추가 적립")],
        "assumptions": ["사망보험금이 (기본보험금 + 계약자적립액)의 형태로 적립액에 연동"],
        "formula": r"\text{사망보험금}_k = \max(\text{기본보험금}, \text{기본보험금}+AV_k)",
        "derivationSteps": [
            step("II-5의 AVₖ(계약자적립액)가 사망보험금 산정에 직접 반영되는 구조를 도입한다 — 이는 6장 I-6에서 다룬 금리연동형 적립액의 실무 응용이다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "금리확정형(II-8)보다 금리연동형이 훨씬 복잡한 이유는, 부채(사망보험금)의 크기 자체가 매월 갱신되는 적립액에 의존하기 때문이다 — 이것이 I-10의 확률론적 시나리오가 필요해지는 근본 이유이기도 하다.",
        "relatedFormulas": "6장 I-6, II-5의 응용.",
        "prerequisites": ["II-5 금리연동형 UL종신보험의 개요", "6장 I-6 금리연동형보험의 계약자적립액"],
        "leadsTo": ["II-10 금리연동형상품 Case1의 보험부채 시가평가"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.9 변동수수료모형"], "기초항목(공시이율) 성과에 연동되는 이 급부구조가 변동수수료모형(VFA) 적용 대상 상품의 전형적인 예다."),
    },
    {
        "num": "II-10", "title": "금리연동형상품 Case1의 보험부채 시가평가", "page": 1139,
        "def": "II-9의 UL종신보험에 대해, II-8과 같은 완결된 BEL 산출 예시를 제공한다 — 다만 이번에는 I-10의 확률론적 할인율 시나리오가 사용된다.",
        "symbols": [],
        "assumptions": ["최저보증이율 등 옵션성 요소 존재"],
        "formula": r"BEL_0 = \frac{1}{N}\sum_{n=1}^N \sum_{k=1}^n CF_k^n \cdot v^n(k) \cdot \frac{l^{(\tau)}_k}{l^{(\tau)}_0}",
        "derivationSteps": [
            step("II-8과 같은 구조이지만, 금리 시나리오마다 CFₖ(사망보험금이 AVₖ에 의존)와 할인계수 v(k)가 모두 달라지므로, I-10에서처럼 여러 시나리오(n=1,…,N)에 대해 각각 계산한 뒤 평균을 낸다.", r"BEL_0 = \frac{1}{N}\sum_{n=1}^N BEL_0^n"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-8(단일 경로)과 II-10(여러 시나리오 평균)의 비교가 I-9·I-10에서 다룬 결정론적/확률론적 방법의 차이를 실제 숫자로 확인시켜준다.",
        "relatedFormulas": "II-8과 I-10의 결합.",
        "prerequisites": ["II-9 금리연동형상품의 사망보험금과 보너스적립액", "I-10 확률론적 할인율 시나리오"],
        "leadsTo": ["II-11 보험부채 시가평가 정리"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.9 변동수수료모형", "IFRS17 4.5 할인율"]),
    },
    {
        "num": "II-11", "title": "보험부채 시가평가 정리", "page": 1153,
        "def": "11장 전체(월별 다중탈퇴율 → 월별 현금흐름 → 할인율 시나리오 → 현재가치 합산)를 요약하며, 12장(부채 변동분석)으로 넘어가기 위한 발판을 마련한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"BEL_0 \; (\text{11장 완료}) \;\to\; BEL_1, RA_1, CSM_1 \; (\text{12장에서 후속측정})",
        "derivationSteps": [
            step("11장은 '0시점(최초인식)의 부채를 어떻게 평가하는가'를 다뤘다. 다음 장(12장)의 과제는 '이 부채가 시간이 지나며 어떻게 변하고, 그 변동이 어떻게 손익으로 인식되는가'이다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "11장이 '사진 한 장(특정 시점의 부채)'을 찍는 법을 다뤘다면, 12장은 '그 사진들을 이어붙인 동영상(부채의 시간에 따른 변화)'을 다룬다.",
        "relatedFormulas": "11장 전체의 요약, 12장으로의 연결.",
        "prerequisites": ["II-10 금리연동형상품 Case1의 보험부채 시가평가"],
        "leadsTo": ["12장 I-6~8 BEL·RA·CSM 변동분석"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.7.3 보험계약마진의 조정 및 회계처리"], "11장에서 산출한 최초 CSM이 12장에서 어떻게 후속 조정·상각되는지로 이어지는 연결고리다."),
    },
]

data_ch11 = {
    "num": 11, "title": "보험부채 시가평가",
    "summary": "IFRS17 도입에 맞춰 신설된 핵심 장. 1장(할인)·2장(생존확률)·6장(계약자적립액)·9장(다중탈퇴모형)의 이론이 모두 이 장에서 '월별 BEL 산출식'(II-3) 하나로 수렴한다. IFRS17 보험부채 측정을 계리적으로 완전히 구현한다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 11:
        data["chapters"][i] = data_ch11
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 11 upgraded:", len(I) + len(II), "items")
