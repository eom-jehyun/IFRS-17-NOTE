# -*- coding: utf-8 -*-
# 제10장 다중상태모형 — 12-field schema.
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
        "num": "I-1", "title": "확률과정", "titleEn": "stochastic process", "page": 838,
        "def": "시간에 따라 변화하는 확률변수들의 모임. 수학적으로는 {X(t), t≥0}처럼 인덱스 집합 위에 정의된 확률변수족이고, 보험수리학적으로는 '건강→질병→사망'처럼 여러 상태를 오가는 피보험자의 상태변화를 다루기 위한 틀이다.",
        "symbols": [sym("X(t)", "t시점의 상태(확률변수)"), sym("{X(t)}", "확률과정 전체")],
        "assumptions": [],
        "formula": r"\{X(t) : t \ge 0\}",
        "derivationSteps": [
            step("2장의 T(x)가 '단일 사건(사망)까지의 시간'만 다뤘다면, 확률과정은 '시간에 따라 계속 변하는 상태 그 자체'를 다룬다는 점에서 더 일반적인 틀이다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "9장의 다중탈퇴모형이 '탈퇴하면 끝'이라는 일회성 사건이었다면, 다중상태모형은 '상태를 계속 오갈 수 있다'(예: 질병에서 완치되어 건강상태로 복귀)는 점에서 근본적으로 다르다.",
        "relatedFormulas": "2장 II-3 T(x)의 일반화.",
        "prerequisites": ["2장 II-3 (x)의 미래생존기간"],
        "leadsTo": ["I-2 이산시간 마르코프연쇄"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-2", "title": "이산시간 마르코프연쇄", "titleEn": "discrete-time Markov chain", "page": 840,
        "def": "'다음 상태로의 전이확률이 현재 상태에만 의존하고 과거 이력과는 무관하다'는 마르코프 성질을 만족하는 이산시간 확률과정.",
        "symbols": [sym("pᵢⱼ", "상태 i에서 상태 j로 1기간에 전이할 확률")],
        "assumptions": ["마르코프 성질: P(X(t+1)=j | X(t)=i, X(t-1),…) = P(X(t+1)=j | X(t)=i)"],
        "formula": r"P(X(t+1)=j \mid X(t)=i) = p_{ij}",
        "derivationSteps": [
            step("마르코프 성질은 '미래는 오직 현재 상태에만 의존하고, 어떻게 그 상태에 도달했는지(과거 이력)는 상관없다'는 가정이다 — 이는 2장의 생명확률(ₙpₓ가 오직 현재 나이 x에만 의존)에서도 암묵적으로 쓰인 가정이다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "9장의 다중탈퇴모형도 사실 '건강(생존)→사망/해지'라는 매우 단순한(흡수상태만 있는) 마르코프연쇄의 특수사례로 볼 수 있다 — 다중상태모형은 이를 훨씬 일반화한다.",
        "relatedFormulas": "9장 다중탈퇴모형의 일반화.",
        "prerequisites": ["I-1 확률과정", "9장 II-1 다중탈퇴모형"],
        "leadsTo": ["I-3 다중상태모형의 형태"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-3", "title": "다중상태모형의 형태", "page": 854,
        "def": "건강-질병-사망 등 구체적인 상태 구성과, 상태 간 전이가 가능한 방향(예: 질병→사망은 가능하지만 사망→건강은 불가능)을 정의한다.",
        "symbols": [sym("상태공간", "가능한 모든 상태의 집합(예: {건강, 질병, 사망})")],
        "assumptions": ["사망 등 일부 상태는 '흡수상태'(한 번 들어가면 나올 수 없음)"],
        "formula": r"\text{상태공간} = \{0,1,\dots,n\}, \quad \text{사망은 흡수상태}",
        "derivationSteps": [
            step("모형에 포함할 상태들을 정의하고, 각 상태 쌍 사이에 전이가 가능한지(화살표로 표현되는 전이도)를 명시한다 — 예를 들어 '완치'가 가능한 질병이라면 질병→건강 전이가 허용되지만, 9장의 단순 탈퇴모형에서는 이런 복귀가 불가능했다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "9장 다중탈퇴모형의 핵심 한계(탈퇴하면 복귀 불가)를 다중상태모형이 어떻게 극복하는지 보여주는 절이다 — 장기간병보험(LTC)처럼 '악화와 호전을 반복'하는 질병을 다루려면 이 일반화가 필수적이다.",
        "relatedFormulas": "9장 I-1 다중탈퇴잔존표와의 대비.",
        "prerequisites": ["I-2 이산시간 마르코프연쇄"],
        "leadsTo": ["I-4 마르코프연쇄의 적용"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-4", "title": "마르코프연쇄의 적용", "page": 860,
        "def": "실제 건강보험·장기간병보험(LTC) 상품 설계에 마르코프연쇄를 적용하는 사례.",
        "symbols": [],
        "assumptions": [],
        "formula": r"P(\text{상태경로}) = \prod_t p_{X(t),X(t+1)}",
        "derivationSteps": [
            step("마르코프 성질(I-2) 덕분에, 여러 기간에 걸친 특정 상태경로의 확률은 각 단계 전이확률의 단순 곱으로 계산된다.", r"P(\text{경로}) = \prod_t p_{X(t),X(t+1)}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "마르코프 성질이 계산을 극적으로 단순화시킨다 — 아무리 긴 경로라도 각 단계의 곱셈만으로 확률을 구할 수 있다.",
        "relatedFormulas": "I-2의 응용.",
        "prerequisites": ["I-2 이산시간 마르코프연쇄", "I-3 다중상태모형의 형태"],
        "leadsTo": ["I-5 이산시간 마르코프모형과 보험상품의 설계"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-5", "title": "이산시간 마르코프모형과 보험상품의 설계", "page": 881,
        "def": "전이확률행렬을 이용해 실제 건강보험 상품(예: 진단금, 간병비)의 보험료를 산출하는 절차.",
        "symbols": [sym("P", "전이확률행렬(pᵢⱼ를 원소로 하는 행렬)")],
        "assumptions": [],
        "formula": r"APV = \sum_t v^t \sum_i \pi_0(i) \cdot P^t_{i,\text{급부상태}} \cdot (\text{급부액})",
        "derivationSteps": [
            step("초기상태분포 π₀에서 출발해, t기간 후 각 상태에 있을 확률(전이확률행렬의 t제곱, Pᵗ)을 구하고, 급부가 발생하는 상태에 도달할 확률에 급부액과 할인계수를 곱해 합산한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "9장 I-3(다중탈퇴표를 이용한 보험료 계산)의 논리를, 상태가 여러 개이고 복귀가 가능한 훨씬 복잡한 상황으로 확장한 것이다.",
        "relatedFormulas": "9장 I-3의 일반화.",
        "prerequisites": ["I-4 마르코프연쇄의 적용", "9장 I-3 다중탈퇴표를 이용한 보험료 계산"],
        "leadsTo": [],
        "ifrs17": ifrs("간접적 연관", ["IFRS17 4.4 현금흐름"], "복잡한 건강보험 상품의 미래현금흐름 추정에 실무적으로 응용되나, 다중상태모형 자체가 해설서 조문의 대상은 아니다."),
    },
]

II = [
    {
        "num": "II-1", "title": "다중상태모형의 가정", "page": 917,
        "def": "I파트의 이산시간 모형을 연속시간으로 확장하기 위한 가정들 — 전이강도(intensity) μᵢⱼ(t)의 도입.",
        "symbols": [sym("μᵢⱼ(t)", "t시점에 상태 i에서 j로 전이하는 순간율(전이강도)")],
        "assumptions": ["전이강도가 잘 정의된 함수"],
        "formula": r"\mu_{ij}(t) = \lim_{h\to 0^+} \frac{P(X(t+h)=j \mid X(t)=i)}{h}, \quad i\ne j",
        "derivationSteps": [
            step("2장 II-5의 사력 μ(x) 정의(순간사망률)를, '사망'이라는 단일 전이 대신 임의의 두 상태 i→j 사이의 전이에 일반화한다.", r"\mu_{ij}(t) = \lim_{h\to0^+}\frac{P(X(t+h)=j\mid X(t)=i)}{h}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "9장 II-2의 원인별 사력 μ⁽ʲ⁾(x)를 '탈퇴'가 아니라 '상태 간 이동' 전반으로 일반화한 것이 전이강도다.",
        "relatedFormulas": "2장 II-5, 9장 II-2의 일반화.",
        "prerequisites": ["2장 II-5 사력", "9장 II-2 다중탈퇴표"],
        "leadsTo": ["II-3 콜모고로프 전진방정식(KFE)"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "다중상태모형 2", "page": 920,
        "def": "전이확률 ₜpᵢⱼ(t시점 상태 i에서 t+s시점 상태 j에 있을 확률)의 정의와 기본 성질.",
        "symbols": [sym("ₛpᵢⱼ(t)", "t시점 상태 i에서 s기간 후 상태 j에 있을 확률")],
        "assumptions": ["마르코프 성질"],
        "formula": r"{}_sp^{ij}_t = P(X(t+s)=j \mid X(t)=i)",
        "derivationSteps": [
            step("2장 II-3의 ₜpₓ(생존확률)를 상태 i→j 전이확률로 일반화한 정의다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이후 등장하는 콜모고로프 방정식(II-3)이 만족해야 하는 대상이 바로 이 ₛpᵢⱼ(t)다.",
        "relatedFormulas": "2장 II-3의 일반화.",
        "prerequisites": ["II-1 다중상태모형의 가정"],
        "leadsTo": ["II-3 콜모고로프 전진방정식(KFE)"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-3", "title": "콜모고로프 전진방정식(KFE)", "titleEn": "Kolmogorov forward equations", "page": 939,
        "def": "전이확률 ₛpᵢⱼ(t)가 시간(s)에 따라 어떻게 변하는지를 나타내는 미분방정식. 2장 II-7의 미분관계식(d/dt ₜpₓ=−ₜpₓμ(x+t))을 다중상태로 일반화한 것이다.",
        "symbols": [sym("∂/∂s ₛpᵢⱼ(t)", "전이확률의 s에 대한 순간 변화율")],
        "assumptions": ["전이강도 μₖⱼ(t+s)가 정의됨(II-1)"],
        "formula": r"\frac{\partial}{\partial s}\,{}_sp^{ij}_t = \sum_{k\ne j} {}_sp^{ik}_t\,\mu_{kj}(t+s) - {}_sp^{ij}_t \sum_{k\ne j}\mu_{jk}(t+s)",
        "derivationSteps": [
            step("'j상태로 유입되는 흐름'(다른 상태 k에서 j로 들어오는 확률×전이강도의 합)에서 'j상태에서 유출되는 흐름'(j에서 다른 상태로 나가는 확률×전이강도의 합)을 뺀 것이, j상태에 있을 확률의 순간 변화율이라는 흐름보존(flow balance) 논리에서 출발한다.", None),
            step("이를 수식화하면:", r"\frac{\partial}{\partial s}{}_sp^{ij}_t = \sum_{k\ne j} {}_sp^{ik}_t \mu_{kj}(t+s) - {}_sp^{ij}_t\sum_{k\ne j}\mu_{jk}(t+s)"),
            step("2장 II-5의 단순 생존확률(상태가 '생존'/'사망' 둘뿐인 경우)에 이 식을 적용하면, 유입항이 없고(사망은 흡수상태) 유출항만 남아 2장 II-7의 d/dt ₜpₓ=−ₜpₓμ(x+t)로 정확히 환원됨을 확인할 수 있다.", None),
        ],
        "derivation": "",
        "termMeanings": [term("유입항 Σₛpᵢₖμₖⱼ", "다른 상태에서 j상태로 새로 들어오는 확률 흐름"), term("유출항 ₛpᵢⱼΣμⱼₖ", "j상태에서 다른 상태로 빠져나가는 확률 흐름")],
        "intuition": "이 방정식은 물리학의 '흐름 보존 법칙'(유입-유출)과 동일한 사고방식이며, 다중상태모형의 모든 확률 계산이 궁극적으로 이 미분방정식 체계를 푸는 문제로 귀결된다.",
        "relatedFormulas": "2장 II-7의 완전한 일반화. 6장 II-7 Thiele 미분방정식과도 유사한 '유입-유출' 구조.",
        "prerequisites": ["II-2 다중상태모형 2", "2장 II-7 생명표에 관한 함수"],
        "leadsTo": ["II-4 콜모고로프 전진방정식과 다중상태모형"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="이론적으로 6장 II-7(Thiele 미분방정식, IFRS17 부채변동과 개념적으로 연관)과 유사한 구조를 갖지만, 다중상태모형 자체가 해설서 조문의 대상은 아니다."),
    },
    {
        "num": "II-4", "title": "콜모고로프 전진방정식과 다중상태모형", "page": 945,
        "def": "II-3의 방정식을 실제 다중상태모형(예: 3상태 건강보험모형)에 적용해 풀이하는 절.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{연립미분방정식 } \{{}_sp^{ij}_t\}_{i,j} \text{ 를 수치적으로 풀이}",
        "derivationSteps": [
            step("상태 수가 늘어나면 II-3의 방정식이 연립미분방정식 체계가 되며, 보통 해석적으로 풀리지 않아 수치해법(오일러법 등)을 사용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-3 이론의 실무 적용.",
        "relatedFormulas": "II-3의 응용.",
        "prerequisites": ["II-3 콜모고로프 전진방정식(KFE)"],
        "leadsTo": ["II-5 콜모고로프 전진방정식과 다중상태모형 3"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-5", "title": "콜모고로프 전진방정식과 다중상태모형 3", "page": 950,
        "def": "II-4의 적용 사례를 더 복잡한 상태구조로 확장.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{(상태 수가 더 많은 모형에 II-3 반복 적용)}",
        "derivationSteps": [
            step("II-4와 같은 절차를 상태가 더 많은 모형(예: 여러 단계의 질병중증도)에 반복 적용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-4의 심화 사례.",
        "relatedFormulas": "II-4의 확장.",
        "prerequisites": ["II-4 콜모고로프 전진방정식과 다중상태모형"],
        "leadsTo": ["II-6 다중상태모형의 보험료"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-6", "title": "다중상태모형의 보험료", "page": 955,
        "def": "II-3~5의 전이확률을 이용해 다중상태 보험상품의 순보험료를 산출한다 — 5장 I-1의 다중상태 버전.",
        "symbols": [sym("APV(급부)", "특정 상태 도달시 지급되는 급부의 APV"), sym("APV(보험료)", "특정 상태(예: 건강)에 있는 동안 납입하는 보험료의 APV")],
        "assumptions": [],
        "formula": r"P\cdot APV(\text{보험료측 상태연금}) = APV(\text{급부})",
        "derivationSteps": [
            step("5장 I-1의 수지상등원칙(P·äx=Ax)을, '건강상태에 있는 동안 보험료 납입'(연금 구조), '특정 상태 도달시 급부 지급'(보험 구조)이라는 다중상태 버전으로 그대로 적용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "5장의 원리가 형태만 복잡해질 뿐 본질적으로 동일하게 재사용된다는 것을 다시 확인하는 절이다.",
        "relatedFormulas": "5장 I-1의 다중상태 확장.",
        "prerequisites": ["II-3 콜모고로프 전진방정식(KFE)", "5장 I-1 연납평준순보험료"],
        "leadsTo": ["II-7 다중상태모형의 계약자적립액"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-7", "title": "다중상태모형의 계약자적립액", "page": 978,
        "def": "6장의 계약자적립액 이론을 다중상태모형으로 확장 — 특정 상태에 있을 때의 책임준비금 ₜVⁱ.",
        "symbols": [sym("ₜVⁱ", "t시점에 상태 i에 있을 때의 책임준비금")],
        "assumptions": [],
        "formula": r"{}_tV^i = APV_i(\text{미래급부}) - APV_i(\text{미래보험료})",
        "derivationSteps": [
            step("6장 I-1의 장래법을, '현재 상태 i를 조건으로' 하는 다중상태 버전으로 확장한다 — 상태에 따라 잔여 의무가 다르므로 상태별로 별도의 준비금이 필요하다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "6장의 장래법 논리가 '상태별로' 재적용된다는 점이 핵심이다.",
        "relatedFormulas": "6장 I-1의 다중상태 확장.",
        "prerequisites": ["II-6 다중상태모형의 보험료", "6장 I-1 책임준비금의 산출(평가)방법"],
        "leadsTo": [],
        "ifrs17": ifrs("간접적 연관", ["IFRS17 4.1 보험부채 평가를 위한 계약의 분류"], "복잡한 건강보험 상품의 부채평가에 응용될 수 있는 이론적 틀이지만, 해설서가 이 다중상태 접근을 직접 규정하지는 않는다."),
    },
    {
        "num": "II-8", "title": "다중상태모형과 다중탈퇴모형", "page": 990,
        "def": "다중상태모형이 9장의 다중탈퇴모형을 포함하는 더 일반적인 틀임을 공식적으로 증명한다.",
        "symbols": [],
        "assumptions": ["흡수상태만 있고(복귀 불가) 초기상태가 하나뿐인 특수한 다중상태모형"],
        "formula": r"\text{다중탈퇴모형} = \text{다중상태모형} \big|_{\text{모든 탈퇴상태가 흡수상태}}",
        "derivationSteps": [
            step("9장의 다중탈퇴모형은 '건강(단일 초기상태) → {사망, 해지, …}(모두 흡수상태)'라는 특수한 상태구조를 갖는 다중상태모형으로 볼 수 있다는 것을 형식적으로 보인다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "10장 전체가 9장의 일반화라는 것을 공식적으로 확인하는 절이다.",
        "relatedFormulas": "9장 전체와의 관계 정리.",
        "prerequisites": ["9장 I-1 다중탈퇴잔존표(다중탈퇴표)", "I-3 다중상태모형의 형태"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-9", "title": "다중상태모형과 연생모형", "page": 998,
        "def": "8장의 연생모형(두 사람의 결합상태)도 다중상태모형의 특수사례로 볼 수 있음을 보인다 — 상태를 '(둘 다 생존), (x만 생존), (y만 생존), (둘 다 사망)'의 4상태로 정의.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{상태공간} = \{(\text{생존,생존}), (\text{사망,생존}), (\text{생존,사망}), (\text{사망,사망})\}",
        "derivationSteps": [
            step("두 사람의 생사 조합을 4개의 상태로 정의하면, 8장의 T(xy)=min(Tx,Ty), T(x̄y̅)=max(Tx,Ty) 등이 모두 이 4상태 모형의 상태전이로 재해석된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "8장과 9장이 모두 10장이라는 더 일반적인 틀의 특수사례라는 것을 확인하며, 이 책 1~10장 전체의 확률모형이 사실상 하나의 통합된 체계(마르코프 다중상태모형)로 수렴함을 보여준다.",
        "relatedFormulas": "8장 전체와의 관계 정리.",
        "prerequisites": ["8장 II-3 동시생존자상태", "II-8 다중상태모형과 다중탈퇴모형"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-10", "title": "연속시간 마르코프모형과 보험상품의 설계", "page": 1015,
        "def": "I-5(이산시간)의 연속시간 버전 — 실제 복잡한 건강보험 상품을 연속시간 다중상태모형으로 설계·가격산출한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"APV = \int_0^\infty v^t \sum_i \pi_0(i)\, {}_tp^{i,\text{급부상태}}_0 \, (\text{급부율})\, dt",
        "derivationSteps": [
            step("I-5의 이산합을 연속형으로 확장하고, II-3의 콜모고로프 방정식으로 구한 전이확률 ₜpⁱʲ를 대입해 실제 상품의 APV를 계산한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "10장 전체 이론(확률과정→마르코프연쇄→콜모고로프 방정식)이 실무 상품설계로 완결되는 마지막 절이다.",
        "relatedFormulas": "I-5의 연속형 확장, II-3의 응용.",
        "prerequisites": ["I-5 이산시간 마르코프모형과 보험상품의 설계", "II-3 콜모고로프 전진방정식(KFE)"],
        "leadsTo": ["11장 보험부채 시가평가"],
        "ifrs17": ifrs("간접적 연관", ["IFRS17 4.4 현금흐름"], "복잡한 건강보험 상품의 이행현금흐름을 정교하게 추정할 때 응용될 수 있는 심화 이론이지만, IFRS17 자체보다는 계리 가격산출·부채평가 실무의 영역이다."),
    },
]

data_ch10 = {
    "num": 10, "title": "다중상태모형",
    "summary": "마르코프연쇄 기반으로 여러 상태(건강-질병-사망 등) 간 전이를 다루는 모형. 9장 다중탈퇴모형(복귀 불가)과 8장 연생모형(결합상태)이 모두 이 장의 특수사례임이 II-8·II-9에서 밝혀진다. 장기간병보험(LTC), CI보험 등 복잡한 급부 구조의 현금흐름 추정에 사용된다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 10:
        data["chapters"][i] = data_ch10
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 10 upgraded:", len(I) + len(II), "items")
