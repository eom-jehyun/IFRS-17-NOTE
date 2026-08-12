# -*- coding: utf-8 -*-
# 제8장 연생모형 — 12-field schema.
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
        "num": "I-1", "title": "연합생명의 생명확률", "titleEn": "joint-life probabilities", "page": 618,
        "def": "두 명(x세, y세) 이상의 피보험자를 동시에 고려할 때의 생존·사망확률. 수학적으로는 2장 I-3의 생명확률을 두 사람의 결합사건으로 확장한 것이고, 보험수리학적으로는 부부형 보험·유족연금 등 다수 피보험자 상품의 이론적 기초다.",
        "symbols": [sym("(xy)", "x세와 y세 두 사람 모두 생존해야 유지되는 연합상태"), sym("ₙpₓᵧ", "두 사람이 모두 n년 생존할 확률")],
        "assumptions": ["두 사람의 생사가 서로 독립이라고 가정(단순 모형)"],
        "formula": r"{}_np_{xy} = {}_np_x \cdot {}_np_y",
        "derivationSteps": [
            step("독립사건의 결합확률은 각 확률의 곱이라는 확률론의 기본 성질(2장 II-1)에서 출발한다.", None),
            step("'x세와 y세 둘 다 n년 생존'이라는 사건은 두 독립사건의 교집합이므로:", r"{}_np_{xy} = {}_np_x \cdot {}_np_y"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "2장의 단일생명 이론을 그대로 재사용하되, '두 사건이 모두 일어나야 한다'는 조건이 추가된 것뿐이다 — 독립 가정 덕분에 계산이 단순히 곱셈으로 확장된다.",
        "relatedFormulas": "2장 I-3의 확장.",
        "prerequisites": ["2장 I-3 생명확률"],
        "leadsTo": ["I-4 동시생존자 연생연금과 연생보험"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="다수 피보험자 상품(부부형 등)의 이론적 기초이나, 해설서는 상품유형별 세부 계리이론을 규정하지 않는다."),
    },
    {
        "num": "I-2", "title": "연합생명의 사력", "page": 631,
        "def": "연합상태 (xy)의 순간사망률(연합사력) μ(xy) — 둘 중 누구든 먼저 사망하면 연합상태가 종료되므로, 개별 사력의 합으로 표현된다.",
        "symbols": [sym("μ(xy)", "연합상태 (xy)의 사력")],
        "assumptions": ["독립 가정"],
        "formula": r"\mu(xy) = \mu(x) + \mu(y)",
        "derivationSteps": [
            step("독립인 두 사력의 결합에서, '연합상태가 짧은 구간 dt에 종료될 확률'은 'x가 사망하거나 y가 사망하는' 두 배반사건(둘이 동시에 죽을 확률은 dt의 고차항이라 무시)의 합이다.", None),
            step("2장 II-5의 사력 정의를 두 사건에 각각 적용해 더하면:", r"\mu(xy)\,dt \approx \mu(x)\,dt+\mu(y)\,dt \;\Longrightarrow\; \mu(xy)=\mu(x)+\mu(y)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "두 개의 독립적인 '위험원'이 동시에 작동하면, 그 중 하나라도 발생할 순간율은 각 위험률의 단순 합이 된다 — 이는 9장 다중탈퇴모형의 총탈퇴율(q_x^(τ)=Σq_x^(j))과 정확히 같은 논리다.",
        "relatedFormulas": "2장 II-5 사력의 확장. 9장 I-2 다중탈퇴확률과 유사한 가산 구조.",
        "prerequisites": ["2장 II-5 사력", "I-1 연합생명의 생명확률"],
        "leadsTo": ["I-3 조건부 생명확률"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-3", "title": "조건부 생명확률", "page": 636,
        "def": "'x가 y보다 먼저 사망할 확률'처럼, 두 사람 중 누가 먼저 사망하는지에 대한 조건부확률.",
        "symbols": [sym("P(Tx<Ty)", "x가 y보다 먼저 사망할 확률")],
        "assumptions": ["독립 가정"],
        "formula": r"P(T_x < T_y) = \int_0^\infty {}_tp_x\,\mu(x+t)\cdot {}_tp_y \, dt",
        "derivationSteps": [
            step("'x가 정확히 t시점에 사망하고, 그때까지 y는 생존해 있다'는 사건의 확률밀도는 (x가 t시점에 사망할 밀도)×(y가 t시점까지 생존할 확률)이다.", None),
            step("이를 모든 t에 대해 적분하면 'x가 y보다 먼저 사망'할 전체 확률을 얻는다:", r"P(T_x<T_y) = \int_0^\infty {}_tp_x\mu(x+t)\cdot {}_tp_y\,dt"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "유족연금(배우자가 살아있는 동안 지급)을 설계하려면 '누가 먼저 죽는가'에 대한 이 확률이 필수적이다.",
        "relatedFormulas": "I-1, I-2의 응용.",
        "prerequisites": ["I-1 연합생명의 생명확률", "I-2 연합생명의 사력"],
        "leadsTo": ["I-6 조건부 연생보험", "I-7 유족연금"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-4", "title": "동시생존자 연생연금과 연생보험", "titleEn": "joint-life annuity/insurance", "page": 644,
        "def": "두 사람이 '모두' 생존해 있는 동안만 지급되는 연금(동시생존자연금), 또는 '먼저' 사망하는 사람이 발생하는 즉시 지급되는 보험(동시생존자보험).",
        "symbols": [sym("äxy", "동시생존자 연금의 현가율"), sym("Axy", "동시생존자 보험의 현가율")],
        "assumptions": ["독립 가정"],
        "formula": r"\ddot a_{xy} = \sum_{k=0}^{\infty} v^k \cdot {}_kp_{xy}, \qquad A_{xy}=1-d\,\ddot a_{xy}",
        "derivationSteps": [
            step("4장 I-1의 äx 정의(Σvᵏₖpₓ)를, 단일생명 대신 연합상태 (xy)의 생존확률 ₖpₓᵧ(I-1)로 그대로 대체한다:", r"\ddot a_{xy} = \sum_{k=0}^{\infty} v^k\cdot {}_kp_{xy}"),
            step("4장 I-9의 항등식(Ax=1−däx)도 연합상태에 그대로 적용된다 — 이 항등식은 특정 상태의 생존확률 구조에만 의존하므로 단일생명이든 연합생명이든 동일하게 성립한다:", r"A_{xy} = 1-d\,\ddot a_{xy}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "핵심 통찰은 '(xy)를 하나의 새로운 단일생명처럼 취급하면, 3~4장의 모든 공식(Ax, äx, Ax=1−däx 등)을 그대로 재사용할 수 있다'는 것이다. 연생모형 전체가 이 치환 원리 위에 세워져 있다.",
        "relatedFormulas": "3장 I-3, 4장 I-1, 4장 I-9를 (xy)에 그대로 적용.",
        "prerequisites": ["I-1 연합생명의 생명확률", "3장 I-3 사망보험", "4장 I-1 종신연금", "4장 I-9 생명보험과 생명연금의 일시납순보험료의 관계"],
        "leadsTo": ["I-5 최종생존자 연생연금과 연생보험"],
        "ifrs17": ifrs("간접적 연관", note="부부형 연금상품의 미래현금흐름 추정에 사용되나 해설서 특정 조문과 직접 대응되지 않는다."),
    },
    {
        "num": "I-5", "title": "최종생존자 연생연금과 연생보험", "titleEn": "last-survivor annuity/insurance", "page": 650,
        "def": "두 사람 중 '한 명이라도' 생존해 있으면 지급되는 연금(최종생존자연금), 또는 '둘 다' 사망해야 지급되는 보험(최종생존자보험).",
        "symbols": [sym("äx̄ȳ", "최종생존자 연금의 현가율(상태 (x̄y̅))"), sym("ₖpx̄ȳ", "적어도 한 명이 k년 생존할 확률")],
        "assumptions": ["포함배제의 원리(inclusion-exclusion) 적용"],
        "formula": r"{}_kp_{\overline{xy}} = {}_kp_x + {}_kp_y - {}_kp_{xy}",
        "derivationSteps": [
            step("'적어도 한 명 생존'이라는 사건은 'x 생존' 또는 'y 생존'의 합사건이며, 포함배제의 원리(P(A∪B)=P(A)+P(B)−P(A∩B))를 적용한다:", r"{}_kp_{\overline{xy}} = {}_kp_x + {}_kp_y - {}_kp_{xy}"),
            step("이 확률을 I-4와 같은 방식으로 äx̄ȳ, Ax̄ȳ에 대입하면 최종생존자 연금·보험의 현가율을 얻는다.", None),
        ],
        "derivation": "",
        "termMeanings": [term("ₖpₓ+ₖpᵧ−ₖpₓᵧ", "두 사건의 합집합 확률(중복 계산된 교집합을 한 번 빼줌)")],
        "intuition": "부부 중 한 명이 사망해도 남은 배우자에게 연금이 계속 지급되는 '종신연금 보장' 상품이 이 구조를 사용한다.",
        "relatedFormulas": "I-4의 포함배제 확장.",
        "prerequisites": ["I-4 동시생존자 연생연금과 연생보험"],
        "leadsTo": ["I-7 유족연금"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-6", "title": "조건부 연생보험", "page": 660,
        "def": "'x가 y보다 먼저 사망하는 조건 하에서' 지급되는 보험 등, 사망 순서에 조건이 붙는 급부.",
        "symbols": [sym("A¹xy", "x가 y보다 먼저 사망할 때만 지급되는 보험의 현가율")],
        "assumptions": ["독립 가정"],
        "formula": r"A^{\;1}_{xy} = \int_0^\infty v^t \cdot {}_tp_x\,\mu(x+t)\cdot {}_tp_y \, dt",
        "derivationSteps": [
            step("I-3에서 구한 'x가 t시점에 먼저 사망'할 확률밀도에 그 시점의 할인계수를 곱해 적분하면, 이 조건부 급부의 APV를 얻는다.", r"A^{\;1}_{xy} = \int_0^\infty v^t \cdot {}_tp_x\mu(x+t)\cdot {}_tp_y\,dt"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "3장 I-1의 APV 정의(확률×현가의 합)를 순서조건이 있는 사건에 적용한 사례다.",
        "relatedFormulas": "I-3의 응용, 3장 I-1의 재적용.",
        "prerequisites": ["I-3 조건부 생명확률", "3장 I-1 보험료계산의 기초"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-7", "title": "유족연금", "titleEn": "reversionary annuity", "page": 666,
        "def": "x가 먼저 사망한 후, y가 생존해 있는 동안 지급되는 연금(예: 가장 사망 후 배우자에게 지급).",
        "symbols": [sym("äx|y", "x 사망 후 y에게 지급되는 유족연금의 현가율")],
        "assumptions": ["독립 가정"],
        "formula": r"\ddot a_{x|y} = \ddot a_y - \ddot a_{xy}",
        "derivationSteps": [
            step("'y가 생존하는 동안 전부(äy)'에서 '두 사람이 동시에 생존하는 동안(äxy, x가 아직 살아있어 유족연금이 시작되지 않은 기간)'을 빼면, 'x가 먼저 죽은 후 y가 생존하는 기간'만 남는다:", r"\ddot a_{x|y} = \ddot a_y - \ddot a_{xy}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-3(차감법)과 같은 논리 패턴 — 전체에서 겹치는 부분을 빼서 원하는 구간만 남기는 방식이다. 4장 I-3(거치연금)의 차감법과도 구조적으로 동일하다.",
        "relatedFormulas": "I-4, 4장 I-3(거치연금)과 같은 차감 논리.",
        "prerequisites": ["I-4 동시생존자 연생연금과 연생보험", "4장 I-1 종신연금"],
        "leadsTo": [],
        "ifrs17": ifrs("간접적 연관", note="유족연금 상품 설계에 참고되나 해설서 특정 조문과 직접 대응되지 않는다."),
    },
]

II = [
    {
        "num": "II-1", "title": "확률모형의 개요", "page": 679,
        "def": "I파트의 연생이론을 엄밀한 결합확률변수 이론으로 재정립하기 위한 개관.",
        "symbols": [sym("Tx, Ty", "각각 (x), (y)의 미래생존기간(확률변수)")],
        "assumptions": [],
        "formula": r"(T_x, T_y) \sim \text{결합분포}",
        "derivationSteps": [
            step("2장 II-3에서 정의한 T(x)를 두 사람에 대해 동시에 고려하는 결합확률변수 (Tx,Ty)로 확장한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I파트가 직관적 확률 계산으로 연생이론을 다뤘다면, II파트는 이를 확률변수의 결합분포라는 엄밀한 틀로 재구성한다.",
        "relatedFormulas": "2장 II-3의 확장.",
        "prerequisites": ["2장 II-3 (x)의 미래생존기간"],
        "leadsTo": ["II-2 미래생존기간의 결합분포"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "미래생존기간의 결합분포", "page": 680,
        "def": "(Tx,Ty)의 결합분포함수와, 독립 가정 하에서의 결합생존함수.",
        "symbols": [sym("S(s,t)", "Tx>s, Ty>t의 결합생존확률")],
        "assumptions": ["독립 가정 하"],
        "formula": r"S(s,t) = P(T_x>s, T_y>t) = {}_sp_x \cdot {}_tp_y \quad (\text{독립인 경우})",
        "derivationSteps": [
            step("독립사건의 결합확률은 곱이라는 성질(I-1과 동일 원리)을 결합생존함수에 적용한다:", r"S(s,t) = {}_sp_x \cdot {}_tp_y"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-1의 ₙpₓᵧ=ₙpₓₙpᵧ는 사실 이 결합생존함수의 대각선(s=t=n)에 해당하는 특수사례다.",
        "relatedFormulas": "I-1의 엄밀한 재정의.",
        "prerequisites": ["II-1 확률모형의 개요", "I-1 연합생명의 생명확률"],
        "leadsTo": ["II-3 동시생존자상태"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-3", "title": "동시생존자상태", "titleEn": "joint-life status", "page": 685,
        "def": "T(xy)=min(Tx,Ty) — 두 사람 중 먼저 사망하는 시점을 미래생존기간으로 갖는 새로운 '상태' (xy)를 정의한다.",
        "symbols": [sym("T(xy)", "동시생존자상태의 미래생존기간, min(Tx,Ty)")],
        "assumptions": [],
        "formula": r"T(xy) = \min(T_x, T_y)",
        "derivationSteps": [
            step("(xy) 상태는 '둘 다 생존해야 유지'되므로, 둘 중 하나라도 사망하면(더 짧은 쪽이 발생하면) 상태가 종료된다. 따라서 그 생존기간은 두 생존기간의 최솟값이다:", r"T(xy) = \min(T_x,T_y)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-4에서 '(xy)를 새로운 단일생명처럼 취급'한다고 했던 직관을, 여기서 T(xy)=min(Tx,Ty)라는 엄밀한 정의로 뒷받침한다.",
        "relatedFormulas": "I-4의 엄밀한 기반.",
        "prerequisites": ["II-2 미래생존기간의 결합분포"],
        "leadsTo": ["II-4 최종생존자상태"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-4", "title": "최종생존자상태", "titleEn": "last-survivor status", "page": 693,
        "def": "T(x̄y̅)=max(Tx,Ty) — 두 사람 중 나중에 사망하는(마지막까지 생존하는) 시점을 나타내는 상태.",
        "symbols": [sym("T(x̄y̅)", "최종생존자상태의 미래생존기간, max(Tx,Ty)")],
        "assumptions": [],
        "formula": r"T(\overline{xy}) = \max(T_x,T_y), \qquad T(xy)+T(\overline{xy}) = T_x+T_y",
        "derivationSteps": [
            step("'적어도 한 명 생존'은 두 생존기간 중 더 긴 쪽이 끝나야 종료되므로 최댓값이다:", r"T(\overline{xy}) = \max(T_x,T_y)"),
            step("min과 max의 합은 항상 두 원래 값의 합과 같다는 일반적인 수학적 성질(min(a,b)+max(a,b)=a+b)을 이용하면:", r"T(xy)+T(\overline{xy}) = T_x+T_y"),
        ],
        "derivation": "",
        "termMeanings": [term("T(xy)+T(x̄y̅)=Tx+Ty", "이 항등식이 I-5의 äx̄ȳ=äx+äy−äxy(포함배제)의 근본적인 확률론적 근거다")],
        "intuition": "이 min/max 항등식이 I-5에서 다소 기계적으로 적용했던 포함배제 원리의 진짜 이유다 — 결국 '두 상태의 정보를 합치면 원래 두 사람의 정보와 같다'는 자연스러운 사실이다.",
        "relatedFormulas": "I-5 포함배제 원리의 확률론적 근거.",
        "prerequisites": ["II-3 동시생존자상태"],
        "leadsTo": ["II-5 연생변수들의 기대값"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-5", "title": "연생변수들의 기대값", "page": 702,
        "def": "T(xy), T(x̄y̅) 등의 기대값(=평균여명의 연생 버전)을 구한다.",
        "symbols": [sym("e(xy)", "연합상태 (xy)의 평균여명")],
        "assumptions": [],
        "formula": r"e(xy) = \sum_{k=1}^{\infty} {}_kp_{xy}, \qquad e(xy)+e(\overline{xy}) = e_x+e_y",
        "derivationSteps": [
            step("2장 I-4의 평균여명 공식(eₓ=Σₖpₓ)을 연합상태 (xy)에 그대로 적용한다.", r"e(xy) = \sum_{k=1}^\infty {}_kp_{xy}"),
            step("II-4의 min+max 항등식에 기대값을 취하면(기대값의 선형성) 같은 관계가 평균여명에도 성립한다.", r"e(xy)+e(\overline{xy}) = e_x+e_y"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "2장 I-4의 직접적 확장이며, II-4의 min/max 항등식이 평균값 차원에서도 그대로 유지됨을 보여준다.",
        "relatedFormulas": "2장 I-4의 확장.",
        "prerequisites": ["2장 I-4 평균여명", "II-4 최종생존자상태"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-6", "title": "공통충격모형", "titleEn": "common shock model", "page": 708,
        "def": "독립 가정을 완화해, 두 사람에게 동시에 영향을 미치는 공통 위험(예: 교통사고로 부부 동시 사망)을 반영하는 모형.",
        "symbols": [sym("λ", "공통충격(동시사망사건)의 발생률")],
        "assumptions": ["개별 사력 외에 공통충격 λ가 추가로 존재"],
        "formula": r"\mu(xy) = \mu(x)+\mu(y)+\lambda \quad (\text{공통충격 반영 시})",
        "derivationSteps": [
            step("I-2의 독립가정 하 연합사력(μ(x)+μ(y))에, 두 사람에게 동시에 작용하는 공통위험 λ를 추가한다 — 이는 9장의 다중탈퇴모형에서 여러 탈퇴원인을 더하는 논리(q^(τ)=Σq^(j))와 같은 구조다.", r"\mu(xy) = \mu(x)+\mu(y)+\lambda"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "부부가 같은 차를 타고 이동하는 등 실제로는 완전히 독립이 아닌 경우가 있으므로, 이런 종속성을 명시적으로 모형화할 필요가 있다.",
        "relatedFormulas": "I-2의 일반화, 9장 다중탈퇴모형과 유사한 가산 구조.",
        "prerequisites": ["I-2 연합생명의 사력"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-7", "title": "연생보험과 연생연금의 보험수리적 현가", "page": 712,
        "def": "I파트에서 다룬 여러 연생급부의 APV를, II파트의 결합확률변수 정의를 이용해 엄밀하게 재도출한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"A_{xy} = E\!\left[v^{K(xy)+1}\right], \qquad \ddot a_{xy} = E\!\left[\ddot a_{\overline{K(xy)+1}|}\right]",
        "derivationSteps": [
            step("3장 II-1, 4장 II-1에서 다룬 확률변수 기대값 표현(Ax=E[v^(K+1)], äx=E[ä‾(K+1)|])을, 연합상태 (xy)의 K(xy)=⌊T(xy)⌋에 그대로 적용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-4에서 예고했던 '(xy)를 새로운 단일생명처럼 취급'하는 원리가 여기서 완전히 확정된다 — 3~4장의 모든 확률변수 이론이 연합상태에 그대로 이식된다.",
        "relatedFormulas": "3장 II-1, 4장 II-1의 연생 버전.",
        "prerequisites": ["3장 II-1 보험금 연말급", "4장 II-1 연1회 지급의 생명연금", "II-3 동시생존자상태"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-8", "title": "사망률 가정에 따른 보험수리적 현가", "page": 718,
        "def": "독립 가정, 공통충격모형(II-6) 등 서로 다른 사망률 가정 하에서 연생급부의 APV가 어떻게 달라지는지 비교한다.",
        "symbols": [],
        "assumptions": [],
        "formula": r"A_{xy}(\text{독립}) \ne A_{xy}(\text{공통충격 반영})",
        "derivationSteps": [
            step("II-6의 공통충격을 반영하면 연합사력 μ(xy)가 커지므로(λ만큼 추가), 동시생존자상태가 더 빨리 종료되는 경향이 있어 äxy는 작아지고 Axy는 커진다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "가정이 다르면 결과도 달라진다는, 이 책 전체를 관통하는 원칙(전제조건의 중요성)을 연생모형에서 재확인하는 절이다.",
        "relatedFormulas": "II-6, II-7의 비교.",
        "prerequisites": ["II-6 공통충격모형", "II-7 연생보험과 연생연금의 보험수리적 현가"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-9", "title": "조건부 연생보험", "page": 725,
        "def": "I-6을 엄밀한 결합확률 이론으로 재도출.",
        "symbols": [],
        "assumptions": [],
        "formula": r"A^{\;1}_{xy} = \int_0^\infty v^t f_{T_x,T_y}(t,s>t)\,dt",
        "derivationSteps": [
            step("II-2의 결합분포를 이용해 I-6의 조건부 연생보험 APV를 더 일반적인(독립이 아닌 경우도 포함하는) 형태로 다시 유도한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-6의 엄밀화.",
        "relatedFormulas": "I-6의 재도출.",
        "prerequisites": ["I-6 조건부 연생보험", "II-2 미래생존기간의 결합분포"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-10", "title": "유족연금", "page": 731,
        "def": "I-7을 결합확률변수 이론으로 재도출.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\ddot a_{x|y} = \ddot a_y - \ddot a_{xy}",
        "derivationSteps": [
            step("I-7의 차감법을 II파트의 엄밀한 정의 위에서 재확인한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-7의 엄밀화.",
        "relatedFormulas": "I-7의 재도출.",
        "prerequisites": ["I-7 유족연금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-11", "title": "특수한 생존분포", "page": 734,
        "def": "드무아브르 법칙 등 특수 생존분포를 연생모형에 적용했을 때의 닫힌 형태.",
        "symbols": [],
        "assumptions": ["두 사람 모두 같은 드무아브르 법칙(같은 ω)을 따른다고 가정"],
        "formula": r"{}_kp_{xy} = \frac{(\omega-x-k)(\omega-y-k)}{(\omega-x)(\omega-y)}",
        "derivationSteps": [
            step("2장 II-10의 드무아브르 법칙 하 ₖpₓ=(ω−x−k)/(ω−x)를 I-1의 독립곱 공식에 대입한다.", r"{}_kp_{xy} = {}_kp_x\cdot {}_kp_y = \frac{(\omega-x-k)(\omega-y-k)}{(\omega-x)(\omega-y)}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "3장 II-6, 4장 II-8, 6장 II-8과 같은 패턴의 반복 — 특수분포 가정이 복잡한 식을 다항식 형태로 단순화한다.",
        "relatedFormulas": "2장 II-10, I-1의 결합.",
        "prerequisites": ["2장 II-10 사망법칙", "I-1 연합생명의 생명확률"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
]

data_ch8 = {
    "num": 8, "title": "연생모형",
    "summary": "두 명 이상의 피보험자를 대상으로 한 생존분포 이론. 3~4장(단일생명 이론)의 모든 결과가 연합상태(xy)에 그대로 치환 적용된다는 것이 핵심 통찰이다. 연금형/유족보장형 상품의 현금흐름 추정에 사용되며, IFRS17 계약 자체보다는 상품설계·가격산출에 더 가깝다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 8:
        data["chapters"][i] = data_ch8
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 8 upgraded:", len(I) + len(II), "items")
