# -*- coding: utf-8 -*-
# 제9장 다중탈퇴모형 — 12-field schema. 11장의 직접적 선행이론이라 특히 신중하게 작성.
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
        "num": "I-1", "title": "다중탈퇴잔존표(다중탈퇴표)", "titleEn": "multiple decrement table", "page": 746,
        "def": "사망·해지·만기 등 서로 다른 여러 원인(j)으로 계약(또는 사람)이 소멸하는 것을 동시에 추적하는 표. 수학적으로는 2장의 단일탈퇴(사망) 생명표를 여러 탈퇴원인으로 확장한 것이고, 보험수리학적으로는 해지·실효 등 사망 이외의 탈퇴가 흔한 실제 보험계약 관리의 핵심 도구다.",
        "symbols": [sym("l⁽τ⁾ₓ", "x세 시점의 전체 유지자수(모든 탈퇴원인 포함)"), sym("d⁽ʲ⁾ₓ", "x~x+1세 사이 원인 j로 탈퇴한 인원수"), sym("τ", "전체(total)를 나타내는 위첨자"), sym("j", "개별 탈퇴원인을 나타내는 인덱스(예: 1=사망, 2=해지)")],
        "assumptions": ["각 원인별 탈퇴가 상호배타적(동시에 두 원인으로 탈퇴할 수 없음)"],
        "formula": r"l^{(\tau)}_{x+1} = l^{(\tau)}_x - \sum_j d^{(j)}_x",
        "derivationSteps": [
            step("2장 I-2의 생명표 lₓ는 사망이라는 단일 탈퇴원인만 다루었다. 다중탈퇴표는 이를 확장해, x세에 남아있던 인원 l⁽τ⁾ₓ 중 그 해에 각 원인 j별로 d⁽ʲ⁾ₓ명씩 탈퇴한다고 본다.", None),
            step("다음 해에 남는 인원은 전체에서 모든 원인의 탈퇴자를 뺀 값이다:", r"l^{(\tau)}_{x+1} = l^{(\tau)}_x - \sum_j d^{(j)}_x"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "실제 보험계약은 사망뿐 아니라 해지·만기 등 다양한 이유로 없어진다. 다중탈퇴표는 이 모든 '탈퇴'를 동시에 장부에 기록하는 확장된 생명표다.",
        "relatedFormulas": "2장 I-2 생명표의 다중원인 확장.",
        "prerequisites": ["2장 I-2 생명표"],
        "leadsTo": ["I-2 다중탈퇴 확률", "11장 I-5~7 월별 다중탈퇴율 산출"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "IFRS17 미래현금흐름은 사망뿐 아니라 해지 등 여러 탈퇴원인을 동시에 반영해야 하므로, 이 다중탈퇴표가 그 계리적 기초가 된다."),
    },
    {
        "num": "I-2", "title": "다중탈퇴 확률", "page": 747,
        "def": "다중탈퇴표에서 정의되는 원인별 탈퇴확률 q⁽ʲ⁾ₓ와 전체 탈퇴확률 q⁽τ⁾ₓ.",
        "symbols": [sym("q⁽ʲ⁾ₓ", "x세인 사람이 원인 j로 1년 내 탈퇴할 확률"), sym("q⁽τ⁾ₓ", "x세인 사람이 (원인 무관) 1년 내 탈퇴할 확률"), sym("p⁽τ⁾ₓ", "x세인 사람이 1년간 모든 원인에서 생존(유지)할 확률")],
        "assumptions": ["I-1의 다중탈퇴표"],
        "formula": r"q^{(j)}_x = \frac{d^{(j)}_x}{l^{(\tau)}_x}, \qquad q^{(\tau)}_x = \sum_j q^{(j)}_x = \frac{\sum_j d^{(j)}_x}{l^{(\tau)}_x}, \qquad p^{(\tau)}_x = 1-q^{(\tau)}_x",
        "derivationSteps": [
            step("원인별 탈퇴확률은 2장 I-3의 qₓ 정의(dₓ/lₓ)를 각 원인에 그대로 적용한 것이다:", r"q^{(j)}_x = \frac{d^{(j)}_x}{l^{(\tau)}_x}"),
            step("전체 탈퇴확률은 각 원인이 서로 배타적(I-1의 가정)이므로 단순히 더한 것과 같다:", r"q^{(\tau)}_x = \sum_j q^{(j)}_x"),
            step("전체 유지확률은 그 여사건이다:", r"p^{(\tau)}_x = 1-q^{(\tau)}_x"),
        ],
        "derivation": "",
        "termMeanings": [term("q⁽τ⁾ₓ=Σq⁽ʲ⁾ₓ", "여러 위험이 동시에 작용하면 전체 탈퇴율은 각 위험률의 단순 합")],
        "intuition": "이 가산 구조(q⁽τ⁾=Σq⁽ʲ⁾)는 8장 I-2의 연합사력 μ(xy)=μ(x)+μ(y)와 정확히 같은 논리다 — 여러 독립적(배타적) 위험원이 있으면, 그 중 하나라도 발생할 확률(율)은 각각을 단순히 더한 것과 같다.",
        "relatedFormulas": "2장 I-3의 다중원인 확장. 8장 I-2와 같은 가산 구조.",
        "prerequisites": ["I-1 다중탈퇴잔존표(다중탈퇴표)"],
        "leadsTo": ["I-3 다중탈퇴표를 이용한 보험료 계산", "II-3 다중탈퇴율 관련 기본 관계식"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4.5 미래현금흐름의 예측방법"], "사망률·해지율을 각각 별도로(그러나 동시에 작용하는 것으로) 추정해야 한다는 IFRS17의 요구가 이 다중탈퇴확률 구조 위에서 이루어진다."),
    },
    {
        "num": "I-3", "title": "다중탈퇴표를 이용한 보험료 계산", "page": 755,
        "def": "다중탈퇴 확률을 이용해, 사망보험금뿐 아니라 해지환급금까지 포함한 실제 보험상품의 APV를 계산한다.",
        "symbols": [sym("APV", "다중탈퇴 상황을 반영한 보험수리적현가")],
        "assumptions": ["사망시 급부 b^(1), 해지시 급부(해지환급금) b^(2) 등 원인별로 다른 급부가 존재"],
        "formula": r"APV = \sum_{k=0}^{\infty} v^{k+1}\left[b^{(1)}\cdot {}_kp^{(\tau)}_x q^{(1)}_{x+k} + b^{(2)}\cdot {}_kp^{(\tau)}_x q^{(2)}_{x+k} + \cdots \right]",
        "derivationSteps": [
            step("3장 I-1의 APV 정의(확률×현가의 합)를 다중탈퇴 상황에 적용한다 — 이제 '지급될 확률'은 원인별로 다른 급부(b⁽¹⁾, b⁽²⁾,…)에 대응하는 원인별 탈퇴확률로 나뉜다.", None),
            step("k년 유지(전체 탈퇴 기준 ₖp⁽τ⁾ₓ) 후 원인 j로 탈퇴할 확률 ₖp⁽τ⁾ₓ·q⁽ʲ⁾ₓ₊ₖ에 그 원인의 급부 b⁽ʲ⁾를 곱해 모두 더한다:", r"APV = \sum_{k}v^{k+1}\sum_j b^{(j)}\cdot {}_kp^{(\tau)}_x\, q^{(j)}_{x+k}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "실제 보험료 산출에서는 사망보험금뿐 아니라 해지시 돌려줘야 하는 환급금도 회사 입장에서는 '지급'이므로, 이를 함께 반영해야 정확한 보험료가 나온다.",
        "relatedFormulas": "3장 I-1의 다중탈퇴 확장.",
        "prerequisites": ["I-2 다중탈퇴 확률", "3장 I-1 보험료계산의 기초"],
        "leadsTo": [],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "사망보험금·해지환급금 등 여러 원인별 급부를 동시에 현가화하는 이 구조가 IFRS17 이행현금흐름 산출의 계산 골격이다."),
    },
    {
        "num": "I-4", "title": "실무에서 사용되는 다중탈퇴모형", "page": 758,
        "def": "보험 실무에서 흔히 다루는 탈퇴원인(사망, 해지, 장해, 만기 등)의 종류와 각각의 특성을 개관한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"q^{(\tau)}_x = q^{(\text{사망})}_x + q^{(\text{해지})}_x + q^{(\text{장해})}_x + \cdots",
        "derivationSteps": [
            step("I-2의 일반 가산공식을 실제 상품에 등장하는 구체적 탈퇴원인들로 나열한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "실무에서는 상품 종류에 따라 어떤 탈퇴원인을 모형화할지가 다르다(예: 저축성보험은 해지가 중요, 종신보험은 사망이 중요).",
        "relatedFormulas": "I-2의 실무 적용.",
        "prerequisites": ["I-2 다중탈퇴 확률"],
        "leadsTo": ["11장 I-5~7 월별 다중탈퇴율 산출"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4 현금흐름"], "IFRS17이 요구하는 미래현금흐름 추정에 반영해야 하는 계리적 가정(사망률·해지율 등)의 실무적 목록과 직접 대응된다."),
    },
]

II = [
    {
        "num": "II-1", "title": "다중탈퇴모형", "page": 775,
        "def": "I파트의 다중탈퇴표를 확률변수(다중탈퇴 원인 J와 탈퇴시점 K)의 결합분포로 엄밀하게 재정의한다.",
        "symbols": [sym("J", "탈퇴원인(확률변수, 1,2,…)"), sym("K", "탈퇴시점(확률변수)")],
        "assumptions": [],
        "formula": r"P(J=j, K=k) = {}_kp^{(\tau)}_x \cdot q^{(j)}_{x+k}",
        "derivationSteps": [
            step("I-2에서 다룬 '원인별 거치탈퇴확률'을, 두 확률변수(어떤 원인으로, 언제)의 결합확률질량함수로 재정의한다:", r"P(J=j,K=k) = {}_kp^{(\tau)}_x\cdot q^{(j)}_{x+k}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I파트가 직관적 표 계산이었다면, II파트는 이를 두 확률변수(J,K)의 결합분포라는 엄밀한 틀로 재구성한다 — 이후 II-6에서 이 틀을 이용해 APV를 기대값으로 표현한다.",
        "relatedFormulas": "I-2의 엄밀한 재정의.",
        "prerequisites": ["I-2 다중탈퇴 확률"],
        "leadsTo": ["II-3 다중탈퇴율 관련 기본 관계식"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "다중탈퇴표", "page": 786,
        "def": "I-1의 다중탈퇴표를 사력(순간율) 관점에서 재정의 — 원인별 사력 μ⁽ʲ⁾(x)의 개념 도입.",
        "symbols": [sym("μ⁽ʲ⁾(x)", "x세에서 원인 j로 탈퇴할 순간율")],
        "assumptions": [],
        "formula": r"\mu^{(\tau)}(x) = \sum_j \mu^{(j)}(x)",
        "derivationSteps": [
            step("2장 II-5의 사력 정의를 원인별로 확장한다 — 각 원인은 서로 다른 순간율 μ⁽ʲ⁾(x)를 가지며, 전체 탈퇴의 순간율은 이들의 합이다(I-2와 동일한 논리를 연속형으로).", r"\mu^{(\tau)}(x) = \sum_j \mu^{(j)}(x)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-2의 이산형 가산(q⁽τ⁾=Σq⁽ʲ⁾)을 연속형(사력)으로 옮긴 것이며, 8장 I-2의 연합사력과 같은 구조다.",
        "relatedFormulas": "2장 II-5의 다중원인 확장, I-2의 연속형 버전.",
        "prerequisites": ["2장 II-5 사력", "I-2 다중탈퇴 확률"],
        "leadsTo": ["II-4 절대탈퇴율의 계산"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-3", "title": "다중탈퇴율 관련 기본 관계식", "page": 789,
        "def": "ₜp⁽τ⁾ₓ, q⁽ʲ⁾ₓ 등 다중탈퇴 관련 확률들 사이의 관계식을 정리한다.",
        "symbols": [sym("ₜp⁽τ⁾ₓ", "t년간 어떤 원인으로도 탈퇴하지 않을 확률")],
        "assumptions": [],
        "formula": r"{}_tp^{(\tau)}_x = \exp\!\left(-\int_0^t \mu^{(\tau)}(x+s)\,ds\right)",
        "derivationSteps": [
            step("2장 II-7의 ₜpₓ=exp(−∫μ) 공식을, 전체 탈퇴 사력 μ⁽τ⁾(x)에 그대로 적용한다.", r"{}_tp^{(\tau)}_x = \exp\!\left(-\int_0^t \mu^{(\tau)}(x+s)\,ds\right)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "다중탈퇴 상황에서도 '전체(τ)'를 하나의 단일탈퇴처럼 취급하면 2장의 모든 공식이 그대로 재사용된다는 것이 이 절의 핵심이다.",
        "relatedFormulas": "2장 II-7의 재적용.",
        "prerequisites": ["II-2 다중탈퇴표", "2장 II-7 생명표에 관한 함수"],
        "leadsTo": ["II-4 절대탈퇴율의 계산"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-4", "title": "절대탈퇴율의 계산", "titleEn": "absolute rate of decrement / independent rate", "page": 791,
        "def": "'다른 탈퇴원인이 전혀 없다고 가정했을 때'의 단일탈퇴율(절대탈퇴율, 독립탈퇴율) q'⁽ʲ⁾ₓ — 실제 관측되는 다중탈퇴율 q⁽ʲ⁾ₓ와 구분된다.",
        "symbols": [sym("q'⁽ʲ⁾ₓ", "원인 j만 단독으로 존재한다고 가정했을 때의 탈퇴율(절대탈퇴율)"), sym("q⁽ʲ⁾ₓ", "다른 원인들과 경쟁하는 상황에서 실제 관측되는 탈퇴율")],
        "assumptions": ["각 원인의 탈퇴시점이 그 해 안에서 균등분포(UDD)한다고 가정(다중탈퇴판 UDD)"],
        "formula": r"q^{(j)}_x = q'^{(j)}_x \left[1 - \frac{1}{2}\sum_{i\ne j} q'^{(i)}_x + \cdots \right] \approx q'^{(j)}_x\left(1-\tfrac12\sum_{i\ne j}q'^{(i)}_x\right)",
        "derivationSteps": [
            step("실제 관측되는 q⁽ʲ⁾ₓ는 '다른 원인으로 먼저 탈퇴하지 않고 원인 j로 탈퇴할' 확률이므로, 절대탈퇴율 q'⁽ʲ⁾ₓ보다 항상 작거나 같다(다른 원인과 '경쟁'하기 때문).", None),
            step("다중탈퇴판 UDD 가정 하에서, 다른 원인들에 의한 '선점 탈퇴' 효과를 1차 근사하면(2개 원인의 경우를 예로): q⁽ʲ⁾ₓ ≈ q'⁽ʲ⁾ₓ(1−½q'⁽ⁱ⁾ₓ)의 형태로 근사된다.", r"q^{(j)}_x \approx q'^{(j)}_x\left(1-\tfrac12\sum_{i\ne j}q'^{(i)}_x\right)"),
        ],
        "derivation": "",
        "termMeanings": [term("q'⁽ʲ⁾ₓ", "'다른 위험이 아예 없다면' 순수하게 원인 j로만 탈퇴할 확률 — 보험료 산출시 원인별로 독립적인 기초율을 쓰고 싶을 때 필요"), term("q⁽ʲ⁾ₓ", "실제 다중탈퇴표에서 관측되는, 다른 원인과의 경쟁을 반영한 탈퇴율")],
        "intuition": "이것이 이 장에서 가장 중요하고 헷갈리기 쉬운 구분이다 — '해지율만 따로 떼어놓고 보고 싶다'면 절대탈퇴율(q')을, '실제 다중탈퇴표 상의 관측치'를 원한다면 q를 써야 한다. 11장 I-5~7에서 '가격산출용 기초율'과 '부채평가용 기초율'을 구분하는 논리가 바로 이 절대탈퇴율 대 다중탈퇴율의 구분과 정확히 대응된다.",
        "relatedFormulas": "II-2, II-3의 정밀화.",
        "prerequisites": ["II-3 다중탈퇴율 관련 기본 관계식"],
        "leadsTo": ["II-5 다중탈퇴율의 계산", "11장 I-5~7 월별 다중탈퇴율 산출"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4.5 미래현금흐름의 예측방법"], "해설서가 요구하는 '회사 고유 경험통계 기반 최선추정' 사망률·해지율은 실무적으로 이 절대탈퇴율(또는 이와 유사하게 정제된 원인별 독립 기초율) 형태로 추정되어, 11장에서 월별 다중탈퇴율로 재구성된다."),
    },
    {
        "num": "II-5", "title": "다중탈퇴율의 계산", "page": 798,
        "def": "II-4의 근사식을 여러 원인(3개 이상)으로 일반화하고, 절대탈퇴율로부터 다중탈퇴율을 정확히 산출하는 절차를 정리한다.",
        "symbols": [],
        "assumptions": ["다중탈퇴판 UDD"],
        "formula": r"q^{(j)}_x = q'^{(j)}_x \cdot \prod_{i\ne j}\left(1-\tfrac12 q'^{(i)}_x\right) \quad (\text{근사})",
        "derivationSteps": [
            step("II-4의 2원인 근사를 다수 원인으로 확장하면, 각 경쟁 원인에 대해 '선점 탈퇴하지 않을 확률'(1−½q')을 곱한 형태의 근사식을 얻는다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-4의 정밀한 일반화 버전으로, 실무 계산 절차에 해당한다.",
        "relatedFormulas": "II-4의 일반화.",
        "prerequisites": ["II-4 절대탈퇴율의 계산"],
        "leadsTo": ["II-6 다중탈퇴급부의 APV(EPV)"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4.5 미래현금흐름의 예측방법"], "II-4와 동일한 이유로 최선추정 가정 산출의 계산 절차와 직접 관련된다."),
    },
    {
        "num": "II-6", "title": "다중탈퇴급부의 APV(EPV)", "page": 804,
        "def": "I-3을 II파트의 확률변수 틀(II-1의 (J,K))로 엄밀하게 재도출.",
        "symbols": [sym("EPV", "기대현재가치(APV와 동의어로 사용)")],
        "assumptions": [],
        "formula": r"EPV = E\!\left[v^{K+1}\, b^{(J)}\right] = \sum_k \sum_j v^{k+1} b^{(j)}\, {}_kp^{(\tau)}_x\, q^{(j)}_{x+k}",
        "derivationSteps": [
            step("II-1에서 정의한 결합확률변수 (J,K)를 이용해, 급부 b^(J)(원인에 따라 달라짐)의 현재가치 v^(K+1)b^(J)의 기대값으로 I-3의 APV를 다시 표현한다.", r"EPV = E[v^{K+1}b^{(J)}]"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "3장 II-1(Ax=E[v^(K+1)])의 다중탈퇴 확장판이다.",
        "relatedFormulas": "I-3의 엄밀한 재도출, 3장 II-1과 같은 패턴.",
        "prerequisites": ["I-3 다중탈퇴표를 이용한 보험료 계산", "II-1 다중탈퇴모형"],
        "leadsTo": [],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "I-3과 동일한 이유로 이행현금흐름 산출의 이론적 기반이 된다."),
    },
    {
        "num": "II-7", "title": "다중탈퇴모형과 해약급부", "page": 808,
        "def": "해지라는 탈퇴원인에 특화해, 해약환급금이 있는 상품의 APV·책임준비금을 다중탈퇴모형으로 정확히 계산한다.",
        "symbols": [sym("CVₓ₊ₖ", "k년 경과시점 해약환급금(6장 I-3)")],
        "assumptions": ["원인 2를 해지로 설정, 급부 b⁽²⁾=CVₓ₊ₖ"],
        "formula": r"APV(\text{해지급부}) = \sum_k v^{k+1}\,CV_{x+k+1}\, {}_kp^{(\tau)}_x\, q^{(2)}_{x+k}",
        "derivationSteps": [
            step("II-6의 일반식에서 원인 j=2(해지)의 급부를 6장 I-3의 해약환급금 CV로 대체하면, 해지에 따른 기대 지출의 현가를 얻는다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "저축성보험처럼 해지가 빈번한 상품에서는 이 해지급부 APV가 사망급부 APV 못지않게 중요하다.",
        "relatedFormulas": "II-6의 응용, 6장 I-3 해약환급금.",
        "prerequisites": ["II-6 다중탈퇴급부의 APV(EPV)", "6장 I-3 IFRS4 기준의 해약환급금과 IFRS17 기준의 해약환급금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "해지환급금 유출현금흐름은 IFRS17 이행현금흐름의 필수 구성요소(해설서 4.4.1)다."),
    },
    {
        "num": "II-8", "title": "계약의 변경", "titleEn": "policy alterations", "page": 817,
        "def": "감액완납, 연장정기보험 전환 등 계약 조건이 중도에 바뀌는 경우의 다중탈퇴모형 응용.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{변경 후 조건} = f(\text{변경 시점 적립액, 새 급부구조})",
        "derivationSteps": [
            step("계약 변경 시점의 계약자적립액(6장)을 새로운 급부구조에 맞는 일시납보험료로 간주해, 변경 후 조건(보험금액 등)을 역산한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "6장의 적립액 이론과 다중탈퇴모형을 결합한 실무 응용 사례다.",
        "relatedFormulas": "6장 계약자적립액의 응용.",
        "prerequisites": ["6장 I-1 책임준비금의 산출(평가)방법", "II-6 다중탈퇴급부의 APV(EPV)"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-9", "title": "퇴직연금", "page": 820,
        "def": "다중탈퇴모형(사망·퇴직·해고 등)을 퇴직급여 채무 평가에 응용하는 절.",
        "symbols": [],
        "assumptions": ["퇴직·사망·중도퇴사 등을 별도 탈퇴원인으로 모형화"],
        "formula": r"\text{퇴직급여채무} = \sum_k v^k \cdot (\text{급여}) \cdot {}_kp^{(\tau)}_x \cdot q^{(\text{퇴직})}_{x+k}",
        "derivationSteps": [
            step("II-6의 일반식을 퇴직급여라는 급부와 퇴직·사망·중도퇴사라는 탈퇴원인에 적용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "다중탈퇴모형이 보험상품뿐 아니라 기업의 퇴직급여채무(확정급여형 퇴직연금) 평가에도 동일한 원리로 쓰인다는 것을 보여준다.",
        "relatedFormulas": "II-6의 응용.",
        "prerequisites": ["II-6 다중탈퇴급부의 APV(EPV)"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="퇴직급여채무는 IAS19(종업원급여) 영역으로 IFRS17과는 별개 회계기준이다."),
    },
]

data_ch9 = {
    "num": 9, "title": "다중탈퇴모형",
    "summary": "사망·해지·만기 등 여러 탈퇴 원인이 동시에 존재하는 모형. 11장 '보험부채 시가평가'에서 매달 유지자·사망자·해지자 수를 구하는 월별 다중탈퇴율 산출의 직접적 선행 이론이며, 특히 II-4(절대탈퇴율 vs 다중탈퇴율 구분)가 11장의 핵심 논리(가격산출용 vs 부채평가용 기초율)와 정확히 대응된다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 9:
        data["chapters"][i] = data_ch9
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 9 upgraded:", len(I) + len(II), "items")
