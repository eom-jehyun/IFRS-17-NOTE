# -*- coding: utf-8 -*-
# 제7장 영업보험료 — 12-field schema.
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
        "num": "I-1", "title": "영업보험료 산출(I)", "titleEn": "gross premium", "page": 548,
        "def": "5장의 순보험료(급부 원가만 반영)에 사업비를 더해 실제 판매되는 보험료(영업보험료, 총보험료)를 계산한다. 수학적으로는 5장의 수지상등식에 사업비 현가라는 항을 추가한 확장이고, 보험수리학적으로는 이론적 원가와 실제 판매가격을 잇는 다리다.",
        "symbols": [sym("G", "영업보험료(총보험료)"), sym("äx", "보험료연금현가율(4장)"), sym("Ax", "급부현가율(3장)"), sym("e", "사업비(신계약비·유지비 등)의 현가 관련 항")],
        "assumptions": ["사업비가 신계약비(최초 1회성)와 유지비(매년 발생)로 구분됨"],
        "formula": r"G\cdot \ddot a_x = A_x + (\text{사업비의 현가})",
        "derivationSteps": [
            step("5장 I-1의 수지상등식(P·äx=Ax)에서, 보험자가 실제로 부담하는 비용에는 급부(Ax)뿐 아니라 신계약비·유지비 등 사업비도 포함된다는 점을 반영한다.", None),
            step("영업보험료 G는 이 확장된 균형식을 만족해야 한다:", r"G\cdot \ddot a_x = A_x + (\text{사업비의 현가})"),
            step("이를 G에 대해 풀면, G는 5장의 순보험료 P보다 항상 크다(사업비만큼 추가되므로).", r"G = \frac{A_x + (\text{사업비의 현가})}{\ddot a_x} > P"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "순보험료가 '이론적으로 손익분기가 되는 최소 금액'이라면, 영업보험료는 '실제로 회사를 운영하는 데 드는 비용까지 반영한 판매가격'이다.",
        "relatedFormulas": "5장 I-1의 확장.",
        "prerequisites": ["5장 I-1 연납평준순보험료"],
        "leadsTo": ["I-2 영업보험료 산출(II)"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4.2 사업비(보험취득현금흐름, 계약유지비 등)"], "신계약비·유지비 구분은 해설서가 규정하는 보험취득현금흐름(신계약비 성격)과 계약유지비의 구분과 직접 대응된다."),
    },
    {
        "num": "I-2", "title": "영업보험료 산출(II)", "page": 551,
        "def": "사업비 구조를 세분화(신계약비 α, 유지비 β, 수금비 γ 등)해 영업보험료를 더 정밀하게 산출하는 절.",
        "symbols": [sym("α", "신계약비율(초년도 1회성)"), sym("β", "유지비율(매년 발생)"), sym("γ", "수금비율(보험료 대비)")],
        "assumptions": ["각 사업비 항목이 보험금액 또는 보험료에 비례한다고 가정"],
        "formula": r"G\,\ddot a_x = A_x + \alpha + \beta\,\ddot a_x + \gamma\,G\,\ddot a_x",
        "derivationSteps": [
            step("I-1의 '사업비의 현가'를 세 항목으로 분해한다 — 신계약비 α(최초 1회, 연금현가 불필요), 유지비 β(매년 발생하므로 β·äx), 수금비 γ(보험료 자체에 비례하므로 γ·G·äx).", None),
            step("이를 균형식에 대입하고 G에 대해 정리하면:", r"G\,\ddot a_x(1-\gamma) = A_x + \alpha + \beta\,\ddot a_x \;\Longrightarrow\; G = \frac{A_x+\alpha+\beta\,\ddot a_x}{(1-\gamma)\ddot a_x}"),
        ],
        "derivation": "",
        "termMeanings": [term("α", "설계사 수수료 등 계약 체결 자체에 드는 초기 비용"), term("β", "보험증권 유지·관리에 매년 드는 비용"), term("γ", "보험료 수금 자체에 드는 비용(수금비)")],
        "intuition": "실무 보험료 산출은 이렇게 사업비를 성격별로 세분화해 각각 다른 방식(1회성/매년/보험료 비례)으로 반영한다.",
        "relatedFormulas": "I-1의 세분화.",
        "prerequisites": ["I-1 영업보험료 산출(I)"],
        "leadsTo": ["I-3 현금흐름방식의 보험료산출"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4.2 사업비"], "신계약비(α)·유지비(β) 구분이 해설서의 보험취득현금흐름 상각(2.2.5) 논의와 직결된다."),
    },
    {
        "num": "I-3", "title": "현금흐름방식의 보험료산출", "titleEn": "cash flow pricing", "page": 556,
        "def": "예정기초율(고정된 보수적 가정)을 쓰는 대신, 회사가 자체적으로 추정한 최선추정 가정(사망률·해지율·투자수익률·사업비 등)으로 미래현금흐름을 직접 예측해 보험료를 정하는 우리나라의 현행 방식.",
        "symbols": [],
        "assumptions": ["최선추정 가정(과거 예정기초율과 달리 보수적 마진을 별도로 포함하지 않음) 사용"],
        "formula": r"\sum_t (\text{유입현금흐름}_t)\cdot v^t = \sum_t (\text{유출현금흐름}_t)\cdot v^t",
        "derivationSteps": [
            step("I-1·I-2의 Ax, äx 같은 폐쇄형 공식 대신, 매 시점의 현금흐름(보험료 유입, 보험금·해지환급금·사업비 유출)을 개별적으로 예측해 현재가치로 합산하는 방식으로 균형식을 세운다.", r"\sum_t (\text{유입}_t)v^t = \sum_t (\text{유출}_t)v^t"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-1·I-2가 '닫힌 형태의 공식'으로 계산했다면, 현금흐름방식은 '매 시점의 현금흐름을 스프레드시트처럼 하나하나 나열해 더하는' 실무적 접근이다. 두 방식은 이론적으로 동일한 원리(수지상등)를 따르지만, 현금흐름방식이 훨씬 유연하게 다양한 가정을 반영할 수 있다.",
        "relatedFormulas": "I-1의 실무적 일반화(닫힌 형태 대신 개별 현금흐름 나열).",
        "prerequisites": ["I-1 영업보험료 산출(I)"],
        "leadsTo": ["I-4 우리나라의 보험료산출제도", "11장 II-1~4 보험부채 평가모형 개요"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4.5 미래현금흐름의 예측방법"], "현금흐름방식 보험료산출은 예정기초율이 아닌 최선추정 가정을 쓴다는 점에서 IFRS17 이행현금흐름 추정방법과 이미 유사한 사고방식을 취하고 있다. 다만 보험료 산정 목적(가격결정)과 IFRS17 부채평가 목적(결산시점 재측정)은 사용 시점과 용도가 다르다."),
    },
    {
        "num": "I-4", "title": "우리나라의 보험료산출제도", "page": 557,
        "def": "국내 감독규정상 보험료 산출에 적용되는 실무 제도(표준이율, 위험률 조정 한도 등)를 개관한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{보험료} = f(\text{최선추정 가정, 감독규정상 한도})",
        "derivationSteps": [
            step("I-3의 현금흐름방식을 실제 적용할 때 감독당국이 정한 여러 실무 규정(위험률 조정한도, 표준이율 참고 등)이 추가로 작용한다는 것을 개관한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이론(I-1~I-3)과 실제 제도(감독규정) 사이의 간극을 메우는 실무 파트다.",
        "relatedFormulas": "I-3의 제도적 구체화.",
        "prerequisites": ["I-3 현금흐름방식의 보험료산출"],
        "leadsTo": [],
        "ifrs17": ifrs("간접적 연관", note="보험료 산출 감독규정은 회계기준인 IFRS17과 별개 규율체계이지만, 최선추정 가정 사용이라는 공통분모가 있다."),
    },
]

II = [
    {
        "num": "II-1", "title": "영업보험료의 계산", "page": 565,
        "def": "I파트의 영업보험료 산출을 손실 확률변수 L(5장 II-1) 관점에서 재정리한다.",
        "symbols": [sym("L", "영업보험료 기준 손실 확률변수")],
        "assumptions": [],
        "formula": r"L = v^{K(x)+1} + (\text{사업비 관련 현금흐름}) - G\,\ddot a_{\overline{K(x)+1}|}, \qquad E[L]=0",
        "derivationSteps": [
            step("5장 II-1의 L 정의에 사업비 유출을 추가하고, 보험료를 순보험료 P 대신 영업보험료 G로 바꾼다.", r"L = v^{K(x)+1} + (\text{사업비}) - G\,\ddot a_{\overline{K(x)+1}|}"),
            step("E[L]=0 조건에서 I-1·I-2의 결과가 다시 유도된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "5장 II-1의 확장판.",
        "relatedFormulas": "5장 II-1의 확장.",
        "prerequisites": ["5장 II-1 보험료계산의 원칙", "I-1 영업보험료 산출(I)"],
        "leadsTo": ["II-3 미래손실의 분산"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "보험료산출방법과 추가위험산출방법", "page": 569,
        "def": "표준체 위험(일반 생명표)이 아닌 표준하체(추가위험이 있는 피보험자)에 대한 보험료 산출방법 — 연령가산법, 할증법 등.",
        "symbols": [sym("x+k", "연령가산법에서 실제연령 x에 가산연령 k를 더한 산출연령")],
        "assumptions": ["추가위험의 성격(항구적/체감적 등)에 따라 다른 조정방법 적용"],
        "formula": r"\text{연령가산법: } q_{x+k} \text{ 사용} \qquad \text{할증법: } P' = P + (\text{할증보험료})",
        "derivationSteps": [
            step("연령가산법은 '실제 연령보다 몇 살 더 많은 것처럼' 취급해 더 높은 사망률(qₓ₊ₖ)을 적용하는 방식이다.", None),
            step("할증법은 표준 순보험료(5장 I-1)에 추가위험에 상응하는 할증보험료를 단순히 더하는 방식이다:", r"P' = P + (\text{할증보험료})"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "실무에서 건강상태가 표준 이하인 피보험자에게 어떻게 공정한 보험료를 부과할지에 대한 두 가지 접근법을 보여준다.",
        "relatedFormulas": "5장 I-1을 위험조정된 기초율로 재적용.",
        "prerequisites": ["5장 I-1 연납평준순보험료", "2장 I-2 생명표"],
        "leadsTo": [],
        "ifrs17": ifrs("간접적 연관", note="개별계약 위험조정은 보험계약 인수심사(언더라이팅)의 영역으로, IFRS17의 위험조정(RA, 집합 단위의 비금융위험 마진)과는 층위가 다른 개념이다."),
    },
    {
        "num": "II-3", "title": "미래손실의 분산", "titleEn": "variance of future loss", "page": 574,
        "def": "II-1의 손실 확률변수 L의 분산 Var(L)을 구해, 순보험료 산정이 '평균적으로만' 맞을 뿐 개별 계약의 리스크(변동성)는 여전히 남아있음을 정량화한다.",
        "symbols": [sym("Var(L)", "손실 L의 분산")],
        "assumptions": ["5장 II-1의 L=v^(K(x)+1)−P·ä‾(K(x)+1)| 정의 사용"],
        "formula": r"Var(L) = \left(1+\frac{P}{d}\right)^2 \left[{}^2A_x - (A_x)^2\right]",
        "derivationSteps": [
            step("4장 I-9의 항등식(ä‾(K+1)|=(1−v^(K+1))/d)을 이용해 L을 v^(K(x)+1) 하나만의 함수로 정리한다:", r"L = v^{K(x)+1} - P\cdot\frac{1-v^{K(x)+1}}{d} = \left(1+\frac{P}{d}\right)v^{K(x)+1} - \frac{P}{d}"),
            step("L이 v^(K(x)+1)의 1차 선형함수이므로, 분산의 선형변환 공식 Var(aX+b)=a²Var(X)를 적용한다:", r"Var(L) = \left(1+\frac{P}{d}\right)^2 Var\!\left(v^{K(x)+1}\right)"),
            step("Var(v^(K(x)+1))=E[(v^(K(x)+1))²]−(E[v^(K(x)+1)])²이고, 앞항은 이율을 2배(또는 v²을 새로운 할인율로 하는) 'Ax'인 ²Ax(force of interest 2δ 기준 Ax), 뒷항은 (Ax)²이므로:", r"Var(L) = \left(1+\frac{P}{d}\right)^2\left[{}^2A_x-(A_x)^2\right]"),
        ],
        "derivation": "",
        "termMeanings": [term("²Ax", "이력을 2배(2δ)로 하여 계산한 Ax — E[v^(2(K(x)+1))]와 같음"), term("(1+P/d)²", "L을 v^(K(x)+1)의 선형함수로 바꿀 때 생기는 배율의 제곱")],
        "intuition": "E[L]=0(5장)은 '평균적으로 공평하다'는 것만 보장할 뿐, 개별 계약에서는 여전히 큰 손실 또는 이익이 날 수 있다. Var(L)은 이 변동성의 크기를 정량화하며, 계약 건수가 많아질수록(대수의 법칙) 전체 포트폴리오의 상대적 변동성은 작아진다는 보험의 근본 원리(위험분산)를 뒷받침하는 수치다.",
        "relatedFormulas": "5장 II-1의 L 정의, 4장 I-9 항등식의 응용.",
        "prerequisites": ["II-1 영업보험료의 계산", "4장 I-9 생명보험과 생명연금의 일시납순보험료의 관계"],
        "leadsTo": ["II-4 미래손실의 확률", "II-5 백분위 보험료"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.6 위험조정"], "개별계약의 손실 변동성(Var(L))을 정량화하는 이 사고방식이, IFRS17이 요구하는 '비금융위험의 불확실성에 대한 보상'(위험조정 RA) 산출의 통계적 배경이 된다. 다만 RA는 개별계약이 아닌 계약집합 전체의 분포(신뢰수준 기준)를 대상으로 하며 산출방법도 다르다."),
    },
    {
        "num": "II-4", "title": "미래손실의 확률", "page": 582,
        "def": "특정 손실 수준을 넘을 확률 P(L>c)를 구하는 절 — Var(L)을 넘어 손실의 분포 자체를 다룬다.",
        "symbols": [sym("c", "특정 손실 기준값")],
        "assumptions": ["L이 K(x)의 단조함수(1차 선형)라는 II-3의 성질 이용"],
        "formula": r"P(L>c) = P\!\left(K(x) < \frac{\ln[(c+P/d)/(1+P/d)]}{\ln v}\right)",
        "derivationSteps": [
            step("II-3에서 L이 v^(K(x)+1)의 감소함수(v<1이므로 K가 클수록 L은 작아짐)임을 보였다.", None),
            step("따라서 'L>c'라는 사건은 'K(x)가 특정 값보다 작다'는 사건으로 바꿔 쓸 수 있고, 이 임계값은 II-3의 선형식을 K(x)에 대해 역산해 구한다.", None),
            step("K(x)는 이산확률변수이므로, 이 확률은 결국 2장 I-3의 생명확률(ₙqₓ 등)로 계산된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "'손실이 특정 금액을 넘을 확률'은 결국 '사망이 특정 시점보다 일찍 발생할 확률'과 같은 문제로 환원된다 — 이는 II-3의 분산 정보만으로는 알 수 없는, 분포 전체에 대한 정보다.",
        "relatedFormulas": "II-3의 확장(분산→분포).",
        "prerequisites": ["II-3 미래손실의 분산", "2장 I-3 생명확률"],
        "leadsTo": ["II-5 백분위 보험료"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-5", "title": "백분위 보험료", "titleEn": "percentile premium", "page": 591,
        "def": "'손실이 특정 확률(예: 5%) 이하로 발생하도록' 보험료를 정하는 방식 — 순보험료(기대값 기준)와 다른, 신뢰수준 기준 보험료 산정법.",
        "symbols": [sym("Pα", "신뢰수준 α의 백분위 보험료")],
        "assumptions": ["P(L>0) ≤ α (예: α=5%)가 되도록 보험료 결정"],
        "formula": r"P(L>0) \le \alpha \;\Longrightarrow\; P_\alpha \text{ 결정}",
        "derivationSteps": [
            step("II-4의 확률식을 이용해, '손실이 발생할 확률이 α를 넘지 않도록' 하는 최소 보험료를 구한다.", None),
            step("이는 순보험료(E[L]=0, 5장)보다 항상 더 높은 보험료를 요구한다 — 평균적으로 공평한 것을 넘어, 특정 확률 수준까지 안전하게 만들기 때문이다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 접근법은 IFRS17의 위험조정(RA)이 채택하는 신뢰수준(CTE, VaR 등) 접근법과 통계적으로 정확히 같은 아이디어다 — '평균이 아니라 특정 신뢰수준까지 커버되도록 여유를 둔다'는 논리.",
        "relatedFormulas": "II-4의 응용.",
        "prerequisites": ["II-4 미래손실의 확률"],
        "leadsTo": ["II-6 포트폴리오 백분위 보험료 산출원칙"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.6.2 위험조정평가방법"], "신뢰수준(백분위) 기준으로 여유분을 산정하는 이 방법론이, IFRS17 위험조정(RA)의 CTE·VaR 등 신뢰수준 접근법과 통계적으로 동일한 발상이다. 다만 RA는 개별계약이 아닌 계약집합 전체 분포를 대상으로 한다."),
    },
    {
        "num": "II-6", "title": "포트폴리오 백분위 보험료 산출원칙", "page": 597,
        "def": "개별계약이 아닌 전체 포트폴리오(다수 계약의 합)의 총손실에 대해 백분위 원칙을 적용하는 절 — 대수의 법칙에 따라 개별계약보다 훨씬 안정적인 분포를 이용한다.",
        "symbols": [sym("Sₙ", "n개 계약의 총손실(ΣLᵢ)")],
        "assumptions": ["계약들이 독립적이라고 가정(대수의 법칙 적용 가능)"],
        "formula": r"S_n = \sum_{i=1}^n L_i, \qquad E[S_n]=0,\;\; Var(S_n)=\sum_i Var(L_i)",
        "derivationSteps": [
            step("독립인 계약들의 총손실은 각 손실의 합이다:", r"S_n = \sum_{i=1}^n L_i"),
            step("기대값의 선형성과 분산의 독립가산성을 이용하면:", r"E[S_n]=\sum_i E[L_i]=0, \qquad Var(S_n)=\sum_i Var(L_i)"),
            step("계약 수 n이 클수록 Sₙ/n의 분산은 0에 가까워지므로(대수의 법칙), 전체 포트폴리오의 상대적 위험은 개별계약보다 훨씬 작아진다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이것이 보험업의 근본 원리다 — 개별 계약 하나하나는 큰 불확실성을 갖지만(II-3), 많은 계약을 모으면 전체적으로는 예측 가능해진다(대수의 법칙). 이 원리 덕분에 보험자는 II-5의 백분위 보험료를 순보험료에 매우 가깝게 설정해도 안전할 수 있다.",
        "relatedFormulas": "II-3(개별 Var(L))의 포트폴리오 확장.",
        "prerequisites": ["II-3 미래손실의 분산", "II-5 백분위 보험료"],
        "leadsTo": [],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.2.5 보험계약 집합의 구분"], "대수의 법칙에 따른 위험분산이라는 이 원리가, IFRS17이 계약을 '집합(portfolio/cohort)' 단위로 묶어 측정하도록 요구하는 배경 논리(개별계약이 아닌 동질적 위험 집단 단위로 RA·CSM을 산출)와 통한다."),
    },
    {
        "num": "II-7", "title": "영업보험료식 책임준비금", "titleEn": "gross premium reserve", "page": 602,
        "def": "6장의 순보식 책임준비금과 달리, 영업보험료(사업비 포함)를 기준으로 산출하는 책임준비금.",
        "symbols": [sym("ₜVᴳ", "영업보험료식 책임준비금")],
        "assumptions": [],
        "formula": r"{}_tV^G = (A_{x+t} + \text{미래사업비현가}) - G\,\ddot a_{x+t}",
        "derivationSteps": [
            step("6장 I-1의 장래법 논리를, 순보험료 대신 영업보험료 G와 실제 사업비 현금흐름으로 대체해 적용한다.", r"{}_tV^G = (A_{x+t}+\text{미래사업비현가}) - G\,\ddot a_{x+t}"),
            step("영업보험료식 책임준비금은 신계약비를 초년도에 전액 반영하는 순보식과 달리 사업비 지출시기를 실제에 가깝게 반영하므로, 초기에는 순보식보다 낮게(때로는 음수로) 나타날 수 있다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "순보식이 '이론적으로 필요한 최소 준비금'이라면, 영업보험료식은 '실제 현금흐름을 그대로 반영한 준비금'이라는 차이가 있다. 이 개념은 현금흐름방식(I-3)이 실무 표준이 된 이후 IFRS17 이전 시기에 실제 준비금 적정성 평가에 널리 활용되었다.",
        "relatedFormulas": "6장 I-1의 영업보험료 버전.",
        "prerequisites": ["6장 I-1 책임준비금의 산출(평가)방법", "I-1 영업보험료 산출(I)"],
        "leadsTo": ["11장 보험부채 시가평가"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4 현금흐름"], "실제 현금흐름(사업비 포함)을 그대로 반영해 부채를 평가한다는 이 발상이, IFRS17 이행현금흐름이 예정기초율이 아닌 실제·최선추정 현금흐름을 사용한다는 원칙과 개념적으로 가장 가까운 전통이론상의 선례다."),
    },
]

data_ch7 = {
    "num": 7, "title": "영업보험료",
    "summary": "사업비를 포함한 실제 판매 보험료(영업보험료) 산출과 현금흐름방식 보험료산출제도를 다루는 장. IFRS17의 '보험취득현금흐름'과 '유지비' 가정이 이 장의 사업비 이론에서 나온다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 7:
        data["chapters"][i] = data_ch7
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 7 upgraded:", len(I) + len(II), "items")
