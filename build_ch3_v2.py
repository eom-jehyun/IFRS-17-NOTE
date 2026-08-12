# -*- coding: utf-8 -*-
# 제3장 생명보험 — 12-field schema, 전수검사 기준 적용.
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
        "num": "I-1", "title": "보험료계산의 기초", "titleEn": "actuarial present value", "page": 194,
        "def": "보험수리적현가(APV, Actuarial Present Value)의 정의. 수학적으로는 '확률적으로 발생하는 미래 급부'라는 확률변수의 기대값을 현재가치로 계산한 것이고(2장 II-1의 E[g(X)]를 보험금 지급구조에 구체적으로 적용한 것), 보험수리학적으로는 이 값이 곧 보험자가 그 급부를 위해 오늘 확보해두어야 할 자금(순보험료의 기초)이 된다.",
        "symbols": [sym("APV", "보험수리적현가"), sym("v", "할인인자(1장 I-3)"), sym("t", "급부 지급시점")],
        "assumptions": ["급부액과 지급시점이 확률변수(생사에 의존)"],
        "formula": r"APV = E[(\text{지급액}) \times v^{(\text{지급시점})}] = \sum (\text{지급액})\times(\text{할인계수})\times(\text{지급확률})",
        "derivationSteps": [
            step("급부는 '언제 지급되는가(할인)'와 '지급될 확률이 얼마인가(생사)' 두 가지 불확실성을 동시에 갖는다.", None),
            step("2장 II-1의 기대값 정의 E[g(X)]=∫g(x)f(x)dx를, '지급시점에 따라 할인된 지급액'이라는 함수 g에 적용하면 APV의 일반형이 된다:", r"APV = E[g(X)]"),
            step("이산형(연말급)으로 구체화하면, 가능한 모든 지급시점에 대해 (할인계수)×(그 시점에 지급될 확률)×(지급액)을 더한 것이 된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "급부는 '언제(할인)'와 '얼마나 확실하게(확률)' 두 축으로 불확실하다. 두 요소를 곱해 모든 가능한 시나리오에 대해 합산하면 기대현재가치가 되며, 이것이 보험수리학 전체를 관통하는 단일 원리다.",
        "relatedFormulas": "2장 II-1의 E[g(X)]를 급부함수에 특화한 것.",
        "prerequisites": ["1장 I-3 현가와 할인", "2장 II-1 확률이론"],
        "leadsTo": ["I-2 생존보험", "I-3 사망보험"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "IFRS17 최선추정부채(BEL)는 '미래현금흐름을 발생확률과 발생시점을 반영해 현재가치화한 기대값'으로 정의되며, 이는 APV와 수학적으로 동일한 구조다. 다만 IFRS17은 순보험료가 아닌 이행현금흐름 전체(유입-유출)를 대상으로 한다."),
    },
    {
        "num": "I-2", "title": "생존보험", "titleEn": "pure endowment", "page": 195,
        "def": "n년 만기까지 생존해야만 보험금 1을 지급하는 보험(순수생존보험). 수학적으로는 단일 시점 확정급부 1에 생존확률만 곱한 가장 단순한 APV이고, 보험수리학적으로는 저축성보험·연금보험의 만기급부 부분을 구성하는 기본 요소다.",
        "symbols": [sym("A x:n|¹", "x세 가입, n년만기 생존보험의 일시납순보험료(현가율)"), sym("v", "할인인자"), sym("ₙpₓ", "n년 생존확률")],
        "assumptions": ["만기(n년) 시점에 생존해 있어야만 보험금 1 지급, 그 전에 사망하면 아무것도 지급되지 않음"],
        "formula": r"A_{x:\overline{n}|}^{\;1} = v^n \cdot {}_np_x",
        "derivationSteps": [
            step("'n년 후 지급되는 1'을 받으려면 그때까지 생존해야 하므로, I-1의 일반 APV 정의를 이 단일 시나리오에 적용한다.", None),
            step("단일 현금흐름 1의 현가 vⁿ에, 그 현금흐름이 실제로 발생할 확률(=n년 생존확률 ₙpₓ, 2장 I-3)을 곱한다:", r"A_{x:\overline{n}|}^{\;1} = v^n \cdot {}_np_x"),
        ],
        "derivation": "",
        "termMeanings": [term("vⁿ", "n년 후 1원의 현재가치"), term("ₙpₓ", "그 1원을 실제로 받을 확률(=n년 생존)")],
        "intuition": "생사에 관계없이 지급되는 확정연금(1장)과 달리, '생존해야만' 받을 수 있으므로 그 불확실성을 반영해 확정현가에 생존확률을 곱해 깎아준 것이 이 값이다.",
        "relatedFormulas": "I-4 생사혼합보험의 구성요소 중 하나.",
        "prerequisites": ["I-1 보험료계산의 기초", "2장 I-3 생명확률"],
        "leadsTo": ["I-4 생사혼합보험"],
        "ifrs17": ifrs("간접적 연관", note="저축성 상품의 만기급부 구조 이해에 참고되나, 해설서에서 생존보험이라는 상품유형 자체를 별도로 다루지는 않는다."),
    },
    {
        "num": "I-3", "title": "사망보험", "titleEn": "term / whole life insurance", "page": 197,
        "def": "일정기간 내 사망시에만 보험금을 지급하는 정기보험, 또는 평생 언젠가 사망시 지급하는 종신보험. 수학적으로는 발생 가능한 모든 사망시점에 대한 APV의 합(무한급수 또는 유한합)이고, 보험수리학적으로는 순수한 위험보장(사망보장)의 원형이다.",
        "symbols": [sym("Ax", "x세 종신보험의 일시납순보험료(현가율)"), sym("k", "사망이 발생하는 해(0,1,2,…)"), sym("ₖ|qₓ", "k년 거치 후 다음 1년 내 사망확률(2장 I-3)")],
        "assumptions": ["보험금 1을 사망한 해의 연말에 지급(연말급)", "종신보험: 사망시점 제한 없음(평생 보장)"],
        "formula": r"A_x = \sum_{k=0}^{\infty} v^{k+1} \cdot {}_{k|}q_x",
        "derivationSteps": [
            step("k번째 해에 사망한다는 사건의 확률은 2장 I-3의 거치사망확률 ₖ|qₓ이다.", None),
            step("이때 보험금은 사망한 해 말, 즉 k+1시점에 지급되므로 그 현가는 v^(k+1)이다.", None),
            step("가능한 모든 사망시점 k=0,1,2,…에 대해 (현가)×(확률)을 I-1의 APV 정의에 따라 합산하면:", r"A_x = \sum_{k=0}^{\infty} v^{k+1}\cdot {}_{k|}q_x"),
        ],
        "derivation": "",
        "termMeanings": [term("v^(k+1)", "k+1시점(사망한 해의 말)에 지급되는 보험금 1의 현재가치"), term("ₖ|qₓ", "정확히 k번째 해에 사망할 확률")],
        "intuition": "이 급수는 '언젠가는 반드시 사망한다(Σₖ|qₓ=1)'는 사실 때문에 항상 수렴하며, 그 값은 항상 1보다 작다(사망이 늦어질수록 할인 때문에 현가가 작아지므로).",
        "relatedFormulas": "I-4 생사혼합보험의 구성요소. II-1에서 K(x)를 이용해 기대값으로 재정의된다.",
        "prerequisites": ["I-1 보험료계산의 기초", "2장 I-3 생명확률"],
        "leadsTo": ["I-4 생사혼합보험", "II-1 보험금 연말급"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "사망보험금이라는 '확률적 유출현금흐름'을 현재가치화하는 이 구조가 IFRS17 이행현금흐름 중 보장성 급부 추정의 원형이다."),
    },
    {
        "num": "I-4", "title": "생사혼합보험", "titleEn": "endowment insurance", "page": 207,
        "def": "정기사망보험과 생존보험을 결합해, 기간 내 사망하면 그때 보험금을, 만기까지 생존하면 만기에 보험금을 지급하는 상품. 수학적으로는 두 배반사건(사망/생존)에 대한 APV의 단순 합이고, 보험수리학적으로는 보장과 저축이 결합된 대표적인 전통형 상품구조다.",
        "symbols": [sym("A x:n|", "x세 가입, n년만기 생사혼합보험의 현가율"), sym("A x:n|¹ (윗첨자1)", "정기사망보험 부분"), sym("A x:n|¹ (아래첨자, 생존보험 표기)", "생존보험 부분(I-2)")],
        "assumptions": ["n년 내 사망 시 사망한 시점(연말)에 1 지급, n년 만기 생존 시 만기에 1 지급 — 둘 중 정확히 하나만 발생"],
        "formula": r"A_{x:\overline{n}|} = A^{\;1}_{x:\overline{n}|} + A_{x:\overline{n}|}^{\;\;\;1}",
        "derivationSteps": [
            step("생사혼합보험의 급부는 'n년 내 사망하거나, n년까지 생존하거나' 둘 중 하나이며 이 둘은 서로 배반이면서 전체 경우를 모두 포괄한다(반드시 둘 중 하나가 일어남).", None),
            step("배반사건에 대한 기대값은 각 사건의 기대값을 단순히 더한 것과 같으므로(기대값의 선형성), 정기사망보험 부분과 생존보험 부분을 각각 APV로 구해 더하면 된다:", r"A_{x:\overline{n}|} = \underbrace{\sum_{k=0}^{n-1} v^{k+1}\cdot {}_{k|}q_x}_{\text{정기사망보험}} + \underbrace{v^n\cdot {}_np_x}_{\text{생존보험(I-2)}}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "생사혼합보험이 '두 가지 위험을 동시에 대비하는 복잡한 상품'처럼 보이지만, 수학적으로는 이미 알고 있는 두 공식(정기사망보험 + 생존보험)을 단순히 더한 것에 불과하다는 것이 이 항등식의 핵심 통찰이다.",
        "relatedFormulas": "I-2(생존보험) + 정기사망보험(I-3의 유한합 버전)의 합.",
        "prerequisites": ["I-2 생존보험", "I-3 사망보험"],
        "leadsTo": ["I-5 적립보험비용"],
        "ifrs17": ifrs("간접적 연관", note="보장+저축 결합상품 구조 이해에 참고되나, IFRS17 회계처리는 상품유형이 아니라 계약의 현금흐름 특성(투자요소 포함 여부 등, 해설서 2.1.5)에 따라 달라진다."),
    },
    {
        "num": "I-5", "title": "적립보험비용", "titleEn": "cost of insurance decomposition", "page": 208,
        "def": "생사혼합보험의 급부를 '순수보장 부분(위험보험료 대상)'과 '만기까지 반드시 돌려받는 저축 부분(적립보험비용)'으로 분해하는 개념.",
        "symbols": [],
        "assumptions": ["I-4의 생사혼합보험 분해가 성립"],
        "formula": r"\text{생사혼합보험} = \text{정기보험(위험보장)} + \text{순수생존보험(저축)}",
        "derivationSteps": [
            step("I-4의 분해식을 상품설계 관점에서 재해석한다 — 정기사망보험 부분은 '만약 사망하면'이라는 조건부 지급(진짜 위험보장), 생존보험 부분은 '생존만 하면 100% 확정 지급'되는 저축 성격의 요소다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "두 요소 중 생존보험 부분은 사실상 100% 확정 지급되는 저축성 요소이며, 정기보험 부분만이 진정한 '위험'을 담보한다는 통찰을 제공한다. 이 분해는 이후 6장(계약자적립액)에서 순보험료를 위험보험료와 저축보험료로 나누는 논리의 출발점이다.",
        "relatedFormulas": "I-4의 재해석.",
        "prerequisites": ["I-4 생사혼합보험"],
        "leadsTo": ["6장 계약자적립액"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 2.1.5 투자요소"], "보장요소와 저축(투자)요소를 분리하는 이 사고방식은 해설서가 규정하는 '투자요소'(보험사건 발생 여부와 무관하게 상환해야 하는 금액) 식별 논리와 개념적으로 맞닿아 있다."),
    },
    {
        "num": "I-6", "title": "계산기수와 일반식", "titleEn": "commutation functions", "page": 210,
        "def": "Ax 등을 표 계산으로 빠르게 구하기 위해 고안된 옛 실무 도구인 계산기수(commutation function) Cx, Mx, Dx.",
        "symbols": [sym("Cx", "사망급부 계산기수"), sym("Mx", "Cx의 누적합"), sym("Dx", "생존급부 계산기수(=vˣlₓ)"), sym("dx", "x~x+1세 사망자수(2장 I-2)"), sym("lₓ", "x세 생존인원(2장 I-2)")],
        "assumptions": ["연말급 기준"],
        "formula": r"C_x = v^{x+1}\,d_x, \qquad M_x = \sum_{y=x}^{\infty} C_y, \qquad A_x = \frac{M_x}{D_x} \;\; (D_x=v^x l_x)",
        "derivationSteps": [
            step("Ax의 정의식 Σvᵏ⁺¹ₖ|qₓ에서, ₖ|qₓ=dₓ₊ₖ/lₓ(2장 I-3)임을 대입한다:", r"A_x = \sum_{k=0}^\infty v^{k+1}\cdot\frac{d_{x+k}}{l_x}"),
            step("분모 lₓ로 전체를 묶어내고, 분자의 각 항을 vˣ⁺ᵏ⁺¹dₓ₊ₖ의 형태로 맞추기 위해 분자·분모에 vˣ를 곱하면:", r"A_x = \frac{1}{v^x l_x}\sum_{k=0}^\infty v^{x+k+1} d_{x+k}"),
            step("분자의 합을 Cy=v^(y+1)dy의 누적합 Mx로, 분모를 Dx=vˣlₓ로 정의하면 간결한 나눗셈 형태가 된다:", r"A_x = \frac{M_x}{D_x}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "컴퓨터가 없던 시절, Ax·äx 등을 매번 무한급수로 계산하는 대신 미리 계산해둔 계산기수표를 나눗셈 한 번으로 조회할 수 있게 만든 실무적 발명품이다. 현재는 컴퓨터 계산이 보편화되어 이론적 의의가 더 크다.",
        "relatedFormulas": "4장 I-7의 äx=Nx/Dx와 함께 계산기수 체계를 이룬다.",
        "prerequisites": ["I-3 사망보험", "2장 I-2 생명표"],
        "leadsTo": ["4장 I-7 계산기수와 일반식"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="계산기수는 컴퓨터 이전 시대의 계산 실무기법으로, IFRS17 실무(전산 계산 기반)에서는 사용되지 않는다."),
    },
]

II = [
    {
        "num": "II-1", "title": "보험금 연말급", "titleEn": "insurance benefit payable at end of year of death", "page": 215,
        "def": "사망보험금이 사망한 해의 '연말'에 지급되는 경우의 엄밀한 확률모형 정의. I-3의 Ax를 2장 II-4에서 정의한 개산생존기간 K(x)의 함수로 재정의한다.",
        "symbols": [sym("K(x)", "(x)의 미래개산생존기간(2장 II-4)"), sym("v^(K(x)+1)", "K(x)에 따라 정해지는 확률변수(할인된 보험금)")],
        "assumptions": ["보험금은 사망한 해의 연말(K(x)+1시점)에 지급"],
        "formula": r"A_x = E\!\left[v^{K(x)+1}\right] = \sum_{k=0}^{\infty} v^{k+1}\cdot P(K(x)=k)",
        "derivationSteps": [
            step("K(x)가 k라면 지급시점은 항상 k+1이므로, 지급되는 할인된 보험금은 확률변수 v^(K(x)+1)로 나타낼 수 있다.", None),
            step("Ax는 이 확률변수의 기대값이다:", r"A_x = E\left[v^{K(x)+1}\right]"),
            step("이산확률변수의 기대값 정의를 그대로 풀어쓰면, 2장 II-4에서 P(K(x)=k)=ₖ|qₓ임을 이용해 I-3의 식과 정확히 일치함을 확인할 수 있다:", r"A_x = \sum_{k=0}^\infty v^{k+1}P(K(x)=k) = \sum_{k=0}^\infty v^{k+1}\cdot {}_{k|}q_x"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-3에서 급수 형태로 정의했던 Ax를, '확률변수의 기대값'이라는 하나의 표현으로 압축한 것이다. 이후 분산 등 통계량을 다룰 때는 이 확률변수 표현이 훨씬 편리하다(예: Var(v^(K(x)+1)) 계산).",
        "relatedFormulas": "I-3의 엄밀한 재정의.",
        "prerequisites": ["I-3 사망보험", "2장 II-4 (x)의 미래개산생존기간"],
        "leadsTo": ["II-3 보험금 사망즉시급"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "보험금 연말급 (m회분할납)", "page": 228,
        "def": "보험료를 연 m회로 분할납입하되 보험금은 여전히 연말급인 경우 등, 급부·보험료의 지급주기가 다른 일반화된 상황.",
        "symbols": [sym("Ax", "종신보험 현가율(급부는 연말급으로 고정)"), sym("m", "보험료 분할납입 횟수")],
        "assumptions": ["보험금 지급구조는 II-1과 동일(연말급)", "보험료만 연 m회로 분할"],
        "formula": r"A_x \text{ (급부측)은 II-1과 동일; 보험료측 } \ddot a_x^{(m)} \text{만 분할 적용}",
        "derivationSteps": [
            step("이 절 자체는 새 공식을 유도하기보다, '급부는 급부대로(연말급), 보험료는 보험료대로(m회분할)' 각각 독립적으로 정확한 지급구조를 적용해야 한다는 점을 강조한다.", None),
            step("분할납 보험료의 현가율 äx⁽ᵐ⁾는 4장 I-8에서 다루는 개념을 그대로 가져와 쓴다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "실무에서는 보험금(사망시 목돈)과 보험료(매월 납입)의 지급주기가 원래 다른 경우가 많다 — 이 절은 그 두 흐름을 혼동하지 않고 각각 올바른 현가식으로 계산해야 함을 보여준다.",
        "relatedFormulas": "II-1(급부) + 4장 I-8(보험료)의 결합.",
        "prerequisites": ["II-1 보험금 연말급", "4장 I-8 연m회 지급하는 경우의 생명연금"],
        "leadsTo": ["5장 순보험료"],
        "ifrs17": ifrs("간접적 연관", ["IFRS17 4.4 현금흐름"], "보험료(유입)와 보험금(유출)의 지급시점이 서로 다를 수 있다는 인식은 IFRS17 이행현금흐름의 시점별 현금흐름 매핑과 통하지만, 이 절 자체가 특정 조문과 대응되지는 않는다."),
    },
    {
        "num": "II-3", "title": "보험금 사망즉시급", "titleEn": "insurance benefit payable at the moment of death", "page": 232,
        "def": "사망 즉시(그 순간) 보험금이 지급되는, 실제 보험 실무에 더 가까운 가정. 수학적으로는 2장 II-3의 연속형 미래생존기간 T(x)를 이용한 연속형 APV이고, 보험수리학적으로는 실제 보험금 지급 관행(사망신고 후 즉시 지급)에 가장 가까운 모형이다.",
        "symbols": [sym("Āx", "사망즉시급 종신보험의 현가율"), sym("T(x)", "미래생존기간(연속확률변수, 2장 II-3)"), sym("v^T(x)", "사망시점에 따라 정해지는 할인계수")],
        "assumptions": ["보험금은 사망 순간 즉시 지급(연속형)"],
        "formula": r"\bar A_x = E\!\left[v^{T(x)}\right] = \int_0^{\infty} v^t \cdot {}_tp_x \cdot \mu(x+t)\, dt",
        "derivationSteps": [
            step("연말급의 이산합 Σvᵏ⁺¹ₖ|qₓ을 연속시간으로 확장한다 — 'k번째 해 사망'이 '정확히 t시점에서 순간 사망'으로 세분화된다.", None),
            step("순간 t에서 사망할 확률밀도는 2장 II-7에서 다룬 대로 ₜpₓ·μ(x+t)dt이다:", r"P(t<T(x)\le t+dt) \approx {}_tp_x\,\mu(x+t)\,dt"),
            step("이 순간의 급부현가 vᵗ와 곱해 0부터 ∞까지 적분하면:", r"\bar A_x = \int_0^\infty v^t \cdot {}_tp_x\cdot \mu(x+t)\,dt"),
        ],
        "derivation": "",
        "termMeanings": [term("vᵗ", "정확히 t시점에 사망했을 때 그 시점 보험금의 현재가치"), term("ₜpₓμ(x+t)dt", "정확히 t시점 부근에서 사망할 확률밀도")],
        "intuition": "연말급(Ax)이 '그 해가 다 지나야 지급'되는 다소 인위적인 가정이라면, 사망즉시급(Āx)은 실제 보험 실무(사망신고 즉시 보험금 청구·지급)에 훨씬 가까운 모형이다. 다만 이산 생명표(연 단위)로부터 연속형 적분을 정확히 계산하기 어려워 II-4의 근사식이 실무에서 널리 쓰인다.",
        "relatedFormulas": "II-1(연말급)의 연속형 버전. II-4에서 두 값을 서로 근사 변환한다.",
        "prerequisites": ["2장 II-3 (x)의 미래생존기간", "2장 II-7 생명표에 관한 함수"],
        "leadsTo": ["II-4 보험금 사망즉시급과 연말급의 관계"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4 현금흐름"], "실제 지급시점(사망 즉시)을 반영하는 이 모형이 실무 현금흐름 시점 추정의 이론적으로 더 정확한 기준이지만, 해설서 자체는 특정 지급시점 가정을 규정하지 않는다."),
    },
    {
        "num": "II-4", "title": "보험금 사망즉시급과 연말급의 관계", "page": 244,
        "def": "Āx와 Ax를 서로 근사 변환하는 공식 — 실무에서는 사망즉시급이 원칙이지만 계산은 연말급 생명표로 하는 경우가 많아 이 변환이 필수적이다.",
        "symbols": [sym("Āx", "사망즉시급 현가율"), sym("Ax", "연말급 현가율"), sym("i", "연간실이율"), sym("δ", "이력(1장 I-5)")],
        "assumptions": ["UDD(연중 균등분포) 가정 — 한 해 안에서 사망시점이 균등분포한다고 근사"],
        "formula": r"\bar A_x \approx \frac{i}{\delta}\, A_x \quad (\text{UDD 가정 하)}",
        "derivationSteps": [
            step("UDD 가정 하에서는 한 해 안의 사망시점이 균등분포를 이루므로, 평균적으로 그 해의 중간(0.5시점)에 사망한다고 볼 수 있다.", None),
            step("연말(1.0시점)이 아니라 그 중간시점(0.5)에 지급된다고 보정하면, 정확한 보정계수는 이력과 실이율의 비율로 표현되며(UDD 가정 하 표준 결과):", r"\bar A_x \approx \frac{i}{\delta} A_x"),
        ],
        "derivation": "",
        "termMeanings": [term("i/δ", "'기말 기준 이율'과 '연속복리 이력' 사이의 비율로, 항상 1보다 큰 값(i>0인 경우)")],
        "intuition": "i/δ는 항상 1보다 크므로(1장 I-5에서 δ=ln(1+i)<i, i>0인 경우), 이 근사식은 '사망즉시급이 연말급보다 항상 더 비싸다'(더 이른 시점에 지급되므로 덜 할인됨)는 직관과 일치한다.",
        "relatedFormulas": "1장 I-4·I-5의 i, δ 관계를 재사용.",
        "prerequisites": ["1장 I-5 이력과 할인력", "2장 II-9 단수부분에 대한 가정", "II-1 보험금 연말급", "II-3 보험금 사망즉시급"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="근사변환 자체는 계산기법이며, 해설서는 지급시점 근사방법을 규정하지 않는다."),
    },
    {
        "num": "II-5", "title": "재귀식(점화식)", "titleEn": "recursion formula", "page": 251,
        "def": "Ax를 다음 해의 Ax₊₁으로 표현하는 순환 관계식 — 조건부기대값의 법칙(law of total expectation)을 1년 단위로 적용한 결과다.",
        "symbols": [sym("Ax", "x세의 종신보험 현가율"), sym("Ax₊₁", "x+1세의 종신보험 현가율"), sym("qₓ", "x세의 1년 사망확률"), sym("pₓ", "x세의 1년 생존확률")],
        "assumptions": ["연말급 기준"],
        "formula": r"A_x = v\,q_x + v\,p_x\,A_{x+1}",
        "derivationSteps": [
            step("'x세인 사람'의 향후 1년은 두 가지로 갈린다 — 사망(확률 qₓ)하거나 생존(확률 pₓ)하거나.", None),
            step("사망하면 그 즉시(1년 후 시점) 보험금 1을 받으므로 현가는 v·qₓ이다.", None),
            step("생존하면 'x+1세인 사람'과 동일한 상황이 되어, 그 시점(1년 후) 기준 Ax₊₁의 가치를 그대로 이어받되, 이를 현재(0시점) 기준으로 한 번 더 할인해야 하므로 v·pₓ·Ax₊₁이다.", None),
            step("조건부기대값의 법칙에 따라 두 경우를 확률가중 합산하면:", r"A_x = v\,q_x + v\,p_x\,A_{x+1}"),
        ],
        "derivation": "",
        "termMeanings": [term("v·qₓ", "즉시 사망시 지급분의 현가"), term("v·pₓ·Ax₊₁", "생존 후 이어지는 보험의 현가")],
        "intuition": "이 재귀식은 '보험을 1년 단위로 계속 갱신해나간다'는 관점을 수식화한 것이다. 뒤(고령)에서부터 앞으로 계산해나가면(역방향 귀납) 전체 생명표에 대한 Ax를 순차적으로 구할 수 있어 컴퓨터 계산에 매우 효율적이다.",
        "relatedFormulas": "6장 II의 계약자적립액 재귀식과 정확히 같은 논리 구조.",
        "prerequisites": ["I-3 사망보험", "2장 I-3 생명확률"],
        "leadsTo": ["6장 II-5 순보험료의 분해와 재귀식", "12장 I-6~8 BEL 변동분석"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.8 보험부채의 변동"], "'기시 값 → (경과·사건 반영) → 기말 값'이라는 롤포워드 구조가 12장에서 다루는 BEL·RA·CSM 변동분석(기시 부채에서 기말 부채로 넘어가는 과정)과 논리적으로 동일한 패턴이다."),
    },
    {
        "num": "II-6", "title": "특수한 생존분포와 생명보험", "page": 252,
        "def": "2장 II-10~11에서 다룬 드무아브르·곰페르츠·메이컴 법칙을 Ax 계산에 적용했을 때 닫힌 형태(closed form)로 정리되는 특수 사례들.",
        "symbols": [sym("ω", "드무아브르 법칙의 한계연령(2장 II-10)")],
        "assumptions": ["드무아브르 법칙: S(x)=1−x/ω (2장 II-10)"],
        "formula": r"A_x = \frac{\bar a_{\overline{\omega-x}|}}{\omega-x} \quad (\text{드무아브르 법칙, 사망즉시급 근사})",
        "derivationSteps": [
            step("드무아브르 법칙 하에서는 매년 사망확률이 동일(1/(ω−x))하므로, Ax의 무한합이 등가중 형태로 단순화된다.", None),
            step("이 균등한 확률 구조 덕분에 Ax의 급수합이 1장에서 이미 다룬 유한 확정연금(연속형)의 형태로 정확히 정리된다.", r"A_x \approx \frac{\bar a_{\overline{\omega-x}|}}{\omega-x}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "드무아브르 법칙처럼 사망확률이 나이에 관계없이 균등하다는 강한 가정을 두면, 복잡한 보험수리 공식이 이미 알고 있는 이자론 공식(확정연금)으로 환원되는 경우가 있다. 이는 이론 검증이나 근사치 계산에 유용하다.",
        "relatedFormulas": "1장 I-6 확정연금 현가식과의 연결.",
        "prerequisites": ["2장 II-10 사망법칙", "1장 I-6 확정연금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
]

data_ch3 = {
    "num": 3, "title": "생명보험",
    "summary": "사망보험금 등 보험급부의 보험수리적현가(APV)를 계산하는 장. 2장의 확률구조(생존확률·사력)와 1장의 할인이론을 결합해 실제 급부의 가치를 계산한다. IFRS17의 이행현금흐름 중 보험금 유출 현금흐름 추정의 이론적 뼈대다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 3:
        data["chapters"][i] = data_ch3
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 3 upgraded:", len(I) + len(II), "items")
