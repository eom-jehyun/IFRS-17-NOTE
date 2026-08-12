# -*- coding: utf-8 -*-
# 제2장 생존분포와 생명표 — 12-field schema, 전수검사 기준 적용.
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
        "num": "I-1", "title": "확률의 개념", "titleEn": "survival function", "page": 101,
        "def": "생존·사망을 확률변수로 다루기 위한 기초 개념. 수학적으로는 신생아(0세)가 x세를 넘어 생존할 확률을 나타내는 생존함수 S(x)=P(X>x)이고(X는 사망시 나이를 나타내는 확률변수), 보험수리학적으로는 이후 등장하는 모든 생명보험·생명연금의 '지급 여부'를 결정하는 확률적 기반이다.",
        "symbols": [sym("X", "사망시 나이(확률변수)"), sym("x", "특정 나이(상수)"), sym("S(x)", "x세를 넘어 생존할 확률(생존함수)")],
        "assumptions": ["X는 0 이상의 연속확률변수", "S(x)는 x에 대해 비증가함수"],
        "formula": r"S(x) = P(X>x), \qquad S(0)=1, \qquad \lim_{x\to\infty} S(x)=0",
        "derivationSteps": [
            step("'X세에 사망'이라는 사건들은 나이 구간별로 서로 배반이며 전체 나이축을 덮으므로, S(x)는 확률의 공리를 그대로 만족하는 함수여야 한다.", None),
            step("x=0일 때는 '태어나자마자 사망하지 않고 생존'하는 것이 확실하므로:", r"S(0) = P(X>0) = 1"),
            step("x가 한없이 커지면 그 나이를 넘어 생존할 확률은 0에 수렴한다(모든 사람은 유한한 수명을 가짐):", r"\lim_{x\to\infty} S(x) = 0"),
        ],
        "derivation": "",
        "termMeanings": [term("P(X>x)", "확률변수 X(사망나이)가 x보다 클 사건의 확률")],
        "intuition": "S(x)는 '갓 태어난 사람 100명 중 x세까지 살아남는 사람의 비율'이라고 생각하면 된다. 사망은 확률적 사건이므로, 보험수리학은 이를 정확한 시점이 아니라 확률분포로 다룬다.",
        "relatedFormulas": "I-2의 생명표 lₓ는 S(x)를 인원수로 환산한 실무적 표현이다.",
        "prerequisites": [],
        "leadsTo": ["I-2 생명표", "II-2 생존함수(엄밀한 재정의)"],
        "ifrs17": ifrs("간접적 연관", note="생사의 확률적 취급이라는 발상 자체는 IFRS17 미래현금흐름 추정(4.4)의 근저에 있지만, S(x) 자체가 해설서 조문에서 다뤄지지는 않는다."),
    },
    {
        "num": "I-2", "title": "생명표", "titleEn": "life table", "page": 106,
        "def": "생존함수 S(x)를 실무에서 쓰기 쉬운 '인원수' 형태로 바꾼 표. 가상의 신생아 l₀명(예: 100,000명) 중 x세까지 생존한 기대인원수를 lₓ로 나타낸다.",
        "symbols": [sym("l₀", "기준 신생아 수(예: 100,000)"), sym("lₓ", "x세까지 생존한 기대인원수"), sym("dₓ", "x세와 x+1세 사이 사망자수")],
        "assumptions": ["l₀명의 신생아 집단에 대해 대수의 법칙(동질적 집단, 독립적 생사)이 성립한다고 가정"],
        "formula": r"l_x = l_0 \cdot S(x), \qquad d_x = l_x - l_{x+1}",
        "derivationSteps": [
            step("S(x)는 '한 사람이 x세 넘게 살 확률'이므로, l₀명이라는 동질적 집단에 이 확률을 적용하면 기대 생존인원이 된다:", r"l_x = l_0 \cdot S(x)"),
            step("인접한 두 나이의 lₓ 차이가 그 구간(x~x+1세)에서 사망한 인원수다:", r"d_x = l_x - l_{x+1}"),
        ],
        "derivation": "",
        "termMeanings": [term("l₀·S(x)", "확률을 인원수 단위로 환산")],
        "intuition": "S(x)가 추상적인 확률이라면, lₓ는 '실제로 100,000명이 태어났다면 몇 명이 남아있을까'라는 직관적인 숫자로 바꾼 것이다. 보험료 계산 실무에서는 항상 이 lₓ, dₓ 표(생명표)를 기초자료로 사용한다.",
        "relatedFormulas": "I-1의 S(x)를 인원수로 스케일링한 것.",
        "prerequisites": ["I-1 확률의 개념"],
        "leadsTo": ["I-3 생명확률"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4.5 미래현금흐름의 예측방법"], "생명표는 IFRS17이 요구하는 '회사 고유의 경험통계 기반 최선추정 사망률·해지율 가정'을 산출하는 실무 도구의 원형이다."),
    },
    {
        "num": "I-3", "title": "생명확률", "titleEn": "probabilities of life and death", "page": 113,
        "def": "생명표로부터 정의되는 조건부 생존·사망확률. 수학적으로는 조건부확률이고, 보험수리학적으로는 '특정 연령의 사람이 특정 기간 동안 생존/사망할 확률'을 표현하는 가장 기본적인 계산 단위다.",
        "symbols": [sym("ₙpₓ", "x세인 사람이 n년 더 생존할 확률"), sym("ₙqₓ", "x세인 사람이 향후 n년 내 사망할 확률"), sym("ₘ|ₙqₓ", "x세인 사람이 m년 생존 후 그 다음 n년 내 사망할 확률(거치사망확률)"), sym("qₓ", "₁qₓ의 약식 표기(1년 내 사망확률)"), sym("pₓ", "₁pₓ의 약식 표기(1년 생존확률)")],
        "assumptions": ["x, n, m은 0 이상", "lₓ가 I-2에서 정의된 생명표"],
        "formula": r"{}_np_x = \frac{l_{x+n}}{l_x}, \qquad {}_nq_x = 1-{}_np_x = \frac{l_x-l_{x+n}}{l_x}, \qquad {}_{m|n}q_x = \frac{l_{x+m}-l_{x+m+n}}{l_x}",
        "derivationSteps": [
            step("ₙpₓ는 'x세 생존자 lₓ명 중 x+n세까지 생존한 사람의 비율'이라는 조건부확률의 정의 그 자체다:", r"{}_np_x = \frac{l_{x+n}}{l_x}"),
            step("'n년 내 사망'은 'n년 생존'의 여사건이므로:", r"{}_nq_x = 1 - {}_np_x = \frac{l_x - l_{x+n}}{l_x}"),
            step("m년 거치 후 n년 내 사망확률은 'm년 생존(확률 ₘpₓ) 후 그 다음 n년 내 사망(확률 ₙqₓ₊ₘ)'의 결합이므로:", r"{}_{m|n}q_x = {}_mp_x \cdot {}_nq_{x+m}"),
            step("이를 lₓ로 풀어 쓰면:", r"{}_{m|n}q_x = \frac{l_{x+m}}{l_x}\cdot\frac{l_{x+m}-l_{x+m+n}}{l_{x+m}} = \frac{l_{x+m}-l_{x+m+n}}{l_x}"),
        ],
        "derivation": "",
        "termMeanings": [term("ₙpₓ", "n년 뒤까지 살아있을 확률"), term("ₘpₓ·ₙqₓ₊ₘ", "먼저 m년을 생존한 뒤, 그 시점(x+m세)을 기준으로 다시 n년 내 사망할 조건부확률을 곱한 결합확률")],
        "intuition": "모든 생명확률은 결국 'lₓ 표에서 두 시점의 인원수를 비교'하는 것으로 환원된다. 거치확률(ₘ|ₙqₓ)처럼 복잡해 보이는 식도, '생존 확률을 먼저 곱하고 그 다음 조건부 사망확률을 곱한다'는 연쇄법칙을 이해하면 자연스럽게 유도된다.",
        "relatedFormulas": "3장의 사망보험금 현가식 Ax는 이 ₖ|qₓ(=ₖ|₁qₓ)를 매년 더해나가는 구조다.",
        "prerequisites": ["I-2 생명표"],
        "leadsTo": ["I-4 평균여명", "3장 생명보험"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름의 특성과 포함항목", "IFRS17 4.6 위험조정"], "IFRS17 미래현금흐름 추정은 사실상 이 생명확률(정확히는 회사 고유 경험통계로 추정한 버전)에 급부액을 곱해 기대현금흐름을 산출하는 것이다."),
    },
    {
        "num": "I-4", "title": "평균여명", "titleEn": "expectation of life", "page": 116,
        "def": "x세인 사람이 앞으로 생존할 것으로 기대되는 평균 기간. 완전평균여명 e̊ₓ(연속적 잔여수명의 기대값)와 근사평균여명 eₓ(정수년 단위로 근사한 기대값)로 나뉜다.",
        "symbols": [sym("eₓ", "x세의 근사평균여명(정수년 기준)"), sym("e̊ₓ", "x세의 완전평균여명(연속 기준)"), sym("K(x)", "x세인 사람의 미래개산생존기간(정수부분)")],
        "assumptions": ["기대값이 존재할 정도로 lₓ가 충분히 큰 나이에서 0으로 수렴"],
        "formula": r"e_x = \sum_{k=1}^{\infty} {}_kp_x = E[K(x)]",
        "derivationSteps": [
            step("미래생존기간의 정수부분 K(x)는 확률변수이며, 그 기대값은 정의상:", r"e_x = E[K(x)] = \sum_{k=0}^{\infty} k \cdot P(K(x)=k)"),
            step("이산형 확률변수 기대값의 부분합 항등식(Σk·P(K=k) = Σ_{k≥1}P(K≥k))을 적용하면, P(K(x)≥k)=ₖpₓ이므로:", r"e_x = \sum_{k=1}^{\infty} P(K(x)\ge k) = \sum_{k=1}^{\infty} {}_kp_x"),
        ],
        "derivation": "",
        "termMeanings": [term("ₖpₓ", "k년 뒤까지 생존할 확률 — 이 값들을 전부 더하면 기대 생존기간이 된다는 것이 이 항등식의 핵심")],
        "intuition": "평균여명을 직접 'Σk·확률'로 계산하지 않고 'Σ생존확률'로 계산할 수 있는 이유는, 매 1년마다 '그 해까지 생존했다'는 사건 하나하나가 평균 기대값에 1씩 기여하기 때문이다(생존 기간이 길수록 더 많은 항이 더해짐).",
        "relatedFormulas": "I-3의 ₖpₓ를 그대로 재사용하는 응용.",
        "prerequisites": ["I-3 생명확률"],
        "leadsTo": ["4장 생명연금(äx와 유사한 합산 구조)"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="평균여명 자체는 해설서에서 별도로 다루는 계정과목이 아니지만, 종신형 상품의 예상 보장기간을 가늠하는 배경 통계로 실무에서 참고된다."),
    },
    {
        "num": "I-5", "title": "선택표", "titleEn": "select and ultimate table", "page": 119,
        "def": "동일 연령이라도 보험 가입 직후 일정기간(선택기간)은 건강심사 등의 효과로 사망률이 일반 생명표보다 낮게 나타나는 현상(선택효과)을 반영한 표.",
        "symbols": [sym("[x]", "x세에 보험에 가입한 피보험자(선택 시작점)를 나타내는 표기"), sym("l[x]+t", "[x]세에 가입해 t년이 지난 시점의 생존인원(선택표)"), sym("lₓ₊ₜ", "동일 시점의 일반(종국)생명표 생존인원")],
        "assumptions": ["선택기간(보통 수년)이 지나면 선택효과가 사라짐을 가정"],
        "formula": r"l_{[x]+t} \le l_{x+t} \; (\text{선택기간 내}), \qquad l_{[x]+t} = l_{x+t} \; (\text{선택기간 경과 후})",
        "derivationSteps": [
            step("가입심사를 통과한 사람들은 무작위로 뽑은 동일연령 집단보다 평균적으로 건강하다는 선택효과가 존재하므로, 가입 직후에는 사망률이 더 낮다(생존인원이 더 많다):", r"l_{[x]+t} \le l_{x+t}"),
            step("이 효과는 시간이 지나며 점점 희석되고, 선택기간이 끝나면 두 집단 간 건강 차이가 사실상 사라져 두 표가 합류한다:", r"l_{[x]+t} = l_{x+t} \quad (t \ge \text{선택기간})"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "보험에 막 가입한 사람은 심사를 통과했으므로 '평균적인 x세'보다 건강할 가능성이 높다 — 이 정보를 무시하고 일반 생명표만 쓰면 초기 몇 년의 사망률을 과대평가하게 된다.",
        "relatedFormulas": "I-2 생명표의 변형(가입시점 정보를 추가로 반영).",
        "prerequisites": ["I-2 생명표"],
        "leadsTo": [],
        "ifrs17": ifrs("간접적 연관", note="선택효과는 실무 계리가정 산출시 고려되는 요소이나, 해설서 조문에서 별도로 규정하지는 않는다."),
    },
]

II = [
    {
        "num": "II-1", "title": "확률이론", "titleEn": "probability theory", "page": 125,
        "def": "생명표 이론 전체가 의존하는 확률론의 기본 도구 — 확률변수, 결합분포, 조건부확률, 기대값의 법칙(law of total expectation) 등을 보험수리학 맥락에 맞게 재정리한다.",
        "symbols": [sym("g(X)", "확률변수 X(수명 등)에 대한 임의의 함수(예: 급부함수)"), sym("f(x)", "X의 확률밀도함수"), sym("E[·]", "기대값 연산자")],
        "assumptions": ["X는 연속확률변수(밀도함수 f(x) 존재)"],
        "formula": r"E[g(X)] = \int_0^{\infty} g(x) f(x)\, dx",
        "derivationSteps": [
            step("연속확률변수의 함수에 대한 기대값은 정의상 그 함수값에 확률밀도를 곱해 전체 구간에서 적분한 것이다:", r"E[g(X)] = \int_0^\infty g(x) f(x)\,dx"),
        ],
        "derivation": "",
        "termMeanings": [term("g(X)", "이후 3장에서는 보험금 지급함수(예: 사망시점에 따른 할인된 보험금)로 구체화된다")],
        "intuition": "이후 등장하는 모든 보험수리적현가(APV)는 결국 'g(X)의 기대값'이라는 하나의 틀로 통일된다. 이 절은 그 틀 자체를 미리 정리해두는 것이다.",
        "relatedFormulas": "3장 APV 정의의 이론적 기반.",
        "prerequisites": ["I-1 확률의 개념"],
        "leadsTo": ["II-2 생존함수", "3장 보험료계산의 기초"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "생존함수", "titleEn": "survival function (rigorous)", "page": 136,
        "def": "I-1의 S(x)를 확률론적으로 엄밀하게 재정의한다 — S(x)=P(X>x)가 X의 누적분포함수 Fₓ(x)와 정확히 여사건 관계에 있음을 명시한다.",
        "symbols": [sym("Fₓ(x)", "X의 누적분포함수(CDF), P(X≤x)"), sym("S(x)", "생존함수, 1−Fₓ(x)")],
        "assumptions": ["Fₓ가 우연속(right-continuous)인 표준적인 CDF"],
        "formula": r"S(x) = 1 - F_X(x)",
        "derivationSteps": [
            step("X(사망나이)의 CDF는 정의상 P(X≤x)이다:", r"F_X(x) = P(X\le x)"),
            step("'생존'은 '아직 사망하지 않음'의 여사건이므로:", r"S(x) = P(X>x) = 1-F_X(x)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-1에서 직관적으로 도입한 S(x)를, 확률론의 표준 개념(CDF)과 정확히 연결시켜 엄밀성을 확보하는 절이다.",
        "relatedFormulas": "I-1의 재정의.",
        "prerequisites": ["I-1 확률의 개념", "II-1 확률이론"],
        "leadsTo": ["II-3 (x)의 미래생존기간"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-3", "title": "(x)의 미래생존기간", "titleEn": "future lifetime", "page": 139,
        "def": "표기 (x)는 'x세까지 생존한 사람'을 의미하는 기호. 그 사람의 앞으로 남은 생존기간을 확률변수 T(x)로 정의한다.",
        "symbols": [sym("(x)", "x세까지 생존한 사람을 나타내는 기호"), sym("T(x)", "(x)의 미래생존기간(확률변수)"), sym("t", "T(x)가 취할 수 있는 값(경과년수)")],
        "assumptions": ["X>x라는 조건이 이미 주어진 상태(즉 x세까지는 생존이 확인됨)"],
        "formula": r"T(x) = X-x \;\; (X>x \text{ 조건 하)}, \qquad {}_tp_x = P(T(x)>t) = \frac{S(x+t)}{S(x)}",
        "derivationSteps": [
            step("T(x)는 전체 수명 X에서 이미 지나온 나이 x를 뺀 나머지 기간이다:", r"T(x) = X-x"),
            step("ₜpₓ는 조건부확률의 정의(P(A|B)=P(A∩B)/P(B))에 따라, X>x가 주어진 상태에서 X>x+t일 결합확률을 P(X>x)로 나눈 것이다:", r"{}_tp_x = P(T(x)>t) = P(X>x+t \mid X>x) = \frac{P(X>x+t)}{P(X>x)}"),
            step("분자·분모를 생존함수로 바꾸면:", r"{}_tp_x = \frac{S(x+t)}{S(x)}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-3의 ₙpₓ를 생명표(인원수) 대신 생존함수(확률)로 표현한, 수학적으로 더 엄밀한 버전이다. lₓ=l₀S(x)였으므로 두 식은 완전히 같은 값을 준다.",
        "relatedFormulas": "I-3의 ₙpₓ=lₓ₊ₙ/lₓ와 동치(lₓ=l₀S(x) 대입시 동일).",
        "prerequisites": ["II-2 생존함수"],
        "leadsTo": ["II-4 (x)의 미래개산생존기간", "II-5 사력"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-4", "title": "(x)의 미래개산생존기간", "titleEn": "curtate future lifetime", "page": 142,
        "def": "T(x)의 정수부분 K(x)=⌊T(x)⌋ — '앞으로 몇 번째 생일까지 생존하는가'를 나타내는 이산확률변수. 보험금이 연 단위로 지급되는 상품(연말급)을 다룰 때 핵심적으로 쓰인다.",
        "symbols": [sym("K(x)", "(x)의 미래개산생존기간(정수, T(x)의 정수부분)"), sym("k", "K(x)가 취할 수 있는 값(0,1,2,…)")],
        "assumptions": ["T(x)가 II-3에서 정의된 연속확률변수"],
        "formula": r"P(K(x)=k) = {}_kp_x \cdot q_{x+k} = {}_{k|}q_x",
        "derivationSteps": [
            step("K(x)=k라는 사건은 'x+k세까지는 생존하고(ₖpₓ) 그 다음 1년 안에 사망한다(qₓ₊ₖ)'는 사건과 같다:", r"P(K(x)=k) = P(T(x)\ge k \text{ 이고 } T(x)<k+1)"),
            step("이는 조건부확률의 연쇄로 분해된다:", r"P(K(x)=k) = {}_kp_x \cdot q_{x+k}"),
            step("이 값은 I-3에서 정의한 거치사망확률 ₖ|qₓ와 정확히 같다:", r"P(K(x)=k) = {}_{k|}q_x"),
        ],
        "derivation": "",
        "termMeanings": [term("ₖpₓ", "k년까지 생존"), term("qₓ₊ₖ", "그 다음 1년 안에 사망")],
        "intuition": "K(x)는 '연말급 보험금이 몇 년째에 지급되는가'를 결정하는 변수이므로, 3장의 연말급 사망보험금 현가식 Ax를 유도하는 데 직접 사용된다.",
        "relatedFormulas": "I-3의 ₖ|qₓ와 동치. 3장 Ax=E[v^(K(x)+1)]에서 재사용.",
        "prerequisites": ["I-3 생명확률", "II-3 (x)의 미래생존기간"],
        "leadsTo": ["3장 II-1 보험금 연말급"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "연 단위(월 단위로 세분화 가능)로 급부 지급시점을 확률적으로 결정하는 이 변수의 논리가 11장 월별 다중탈퇴율 산출, 나아가 IFRS17 미래현금흐름 시점 추정의 기초가 된다."),
    },
    {
        "num": "II-5", "title": "사력", "titleEn": "force of mortality", "page": 144,
        "def": "특정 순간의 순간사망률(force of mortality) μ(x). 수학적으로는 생존함수의 로그미분에 음수를 취한 것이고, 1장의 이력 δ와 정확히 대칭되는 구조를 가지며, 보험수리학에서 확률적 위험을 다루는 가장 기본적인 순간율 개념이다.",
        "symbols": [sym("μ(x)", "x세의 사력(순간사망률)"), sym("S(x)", "생존함수"), sym("S'(x)", "생존함수의 도함수")],
        "assumptions": ["S(x)가 미분가능"],
        "formula": r"\mu(x) = -\frac{S'(x)}{S(x)} = -\frac{d}{dx}\ln S(x)",
        "derivationSteps": [
            step("짧은 구간 [x, x+dx]에서의 조건부 사망확률을 μ(x)dx로 정의한다:", r"P(x<X\le x+dx \mid X>x) \approx \mu(x)\,dx"),
            step("이 조건부확률은 [S(x)−S(x+dx)]/S(x)이고, dx→0 극한에서 분자가 −S'(x)dx로 근사되므로:", r"\mu(x)\,dx \approx \frac{-S'(x)\,dx}{S(x)} \;\Longrightarrow\; \mu(x) = -\frac{S'(x)}{S(x)}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "1장에서 δ=a'(t)/a(t)로 정의했던 이력과 정확히 같은 구조이지만 부호가 반대다 — a(t)는 증가함수(종가), S(x)는 감소함수(생존확률)이기 때문이다. '화폐가 불어나는 순간속도'와 '생존확률이 줄어드는 순간속도'가 수학적으로 쌍둥이 개념이라는 점이 이자론과 생명표 이론을 잇는 다리다.",
        "relatedFormulas": "1장 I-5의 이력 δ=a'(t)/a(t)와 부호 반대의 대칭 구조.",
        "prerequisites": ["II-2 생존함수", "1장 I-5 이력과 할인력"],
        "leadsTo": ["II-6 생명표(μ와 lₓ의 관계)", "II-7 생명표에 관한 함수"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4.5 미래현금흐름의 예측방법", "IFRS17 4.6 위험조정"], "μ(x)는 실무적으로 이산화된 qₓ 형태로 쓰이지만, 그 이론적 배경은 이 순간사망률 개념이다. IFRS17 미래현금흐름 추정과 위험조정 산출 모두 이 확률구조를 전제로 한다."),
    },
    {
        "num": "II-6", "title": "생명표 (μ와 lₓ의 관계)", "page": 152,
        "def": "사력 μ(x)와 생명표 lₓ 사이의 관계를 공식화한다. lₓ가 μ(x)의 적분으로 표현될 수 있음을 보인다.",
        "symbols": [sym("l'ₓ", "lₓ의 (x에 대한) 도함수"), sym("l₀", "기준 신생아 수")],
        "assumptions": ["lₓ = l₀S(x) (I-2)가 미분가능"],
        "formula": r"\mu(x) = -\frac{l_x'}{l_x}, \qquad l_x = l_0 \exp\!\left(-\int_0^x \mu(s)\,ds\right)",
        "derivationSteps": [
            step("lₓ=l₀S(x)이므로 μ(x)=−S'(x)/S(x)에 그대로 대입하면(l₀는 상수라 미분에 영향 없음):", r"\mu(x) = -\frac{l_x'}{l_x}"),
            step("이 식을 0부터 x까지 적분하면:", r"\int_0^x \mu(s)\,ds = -\int_0^x \frac{l_s'}{l_s}\,ds = -\big[\ln l_s\big]_0^x = \ln l_0 - \ln l_x"),
            step("이를 lₓ에 대해 정리하면:", r"l_x = l_0 \exp\!\left(-\int_0^x \mu(s)\,ds\right)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "1장의 a(t)=e^(∫δ)와 정확히 같은 구조다 — 순간율(μ 또는 δ)을 적분해 지수함수 안에 넣으면 누적된 결과(lₓ 또는 a(t))를 얻는다는 것이 두 이론의 공통 패턴이다.",
        "relatedFormulas": "1장 I-5의 a(t)=e^(∫δ)와 대칭.",
        "prerequisites": ["II-5 사력", "I-2 생명표"],
        "leadsTo": ["II-7 생명표에 관한 함수"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-7", "title": "생명표에 관한 함수", "page": 154,
        "def": "μ(x), ₜpₓ, ₜqₓ 등을 서로 유도해내는 관계식 모음 — 사력으로부터 생존확률을 구하는 적분식과 그 미분관계.",
        "symbols": [sym("ₜpₓ", "x세인 사람의 t년 생존확률"), sym("μ(x+s)", "x+s세의 사력")],
        "assumptions": ["μ가 [x,x+t] 구간에서 적분가능"],
        "formula": r"{}_tp_x = \exp\!\left(-\int_0^t \mu(x+s)\,ds\right), \qquad \frac{d}{dt}\,{}_tp_x = -{}_tp_x \cdot \mu(x+t)",
        "derivationSteps": [
            step("ₜpₓ=S(x+t)/S(x)이고, II-6에서 S(x)=exp(−∫₀ˣμ)를 얻었으므로 이를 대입하면:", r"{}_tp_x = \frac{\exp\left(-\int_0^{x+t}\mu\right)}{\exp\left(-\int_0^x \mu\right)} = \exp\!\left(-\int_x^{x+t}\mu(u)\,du\right)"),
            step("적분 구간을 u=x+s로 치환하면:", r"{}_tp_x = \exp\!\left(-\int_0^t \mu(x+s)\,ds\right)"),
            step("이를 t로 미분하면(지수함수의 미분과 사력의 정의를 이용):", r"\frac{d}{dt}\,{}_tp_x = -{}_tp_x\cdot\mu(x+t)"),
        ],
        "derivation": "",
        "termMeanings": [term("−ₜpₓ·μ(x+t)", "t시점까지 생존한 상태에서, 그 순간의 사망위험만큼 생존확률이 줄어드는 속도")],
        "intuition": "이 미분관계식은 12장에서 다루는 '보험부채가 순간마다 사망위험만큼씩 소진된다'는 개념과 논리적으로 유사한 구조를 가진다.",
        "relatedFormulas": "II-3(ₜpₓ의 정의), II-5(μ의 정의)의 결합.",
        "prerequisites": ["II-3 (x)의 미래생존기간", "II-5 사력", "II-6 생명표"],
        "leadsTo": ["II-8 사력과 평균여명의 근사치"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-8", "title": "사력과 평균여명의 근사치", "page": 166,
        "def": "생명표가 정수 나이에서만 주어질 때, 그 사이(단수부분, 0<s<1)의 사력을 근사하는 방법. UDD(연중 균등분포) 가정이 대표적이다.",
        "symbols": [sym("s", "0과 1 사이의 소수 나이(단수부분)"), sym("qₓ", "x세의 1년 사망확률"), sym("μ(x+s)", "단수부분 나이 x+s에서의 근사 사력")],
        "assumptions": ["UDD(Uniform Distribution of Deaths) 가정: 한 살 구간 안에서 사망시점이 균등분포한다고 가정"],
        "formula": r"\mu(x+s) \approx \frac{q_x}{1-s\,q_x}, \qquad 0\le s<1",
        "derivationSteps": [
            step("UDD 가정 하에서는 lₓ₊ₛ가 s에 대해 선형이라고 가정한다:", r"l_{x+s} = l_x - s\,d_x"),
            step("사력의 정의 μ(x+s)=−l'ₓ₊ₛ/lₓ₊ₛ에 이 선형식을 대입한다. l'ₓ₊ₛ(s에 대한 도함수)는 −dₓ로 상수이므로:", r"\mu(x+s) = \frac{d_x}{l_x - s\,d_x}"),
            step("분자·분모를 lₓ로 나누고 qₓ=dₓ/lₓ를 대입하면:", r"\mu(x+s) = \frac{q_x}{1-s\,q_x}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "정수년 단위로만 주어진 생명표를 '월별'처럼 더 세밀한 단위로 쪼개 쓰려면 이런 보간 가정이 필요하다. 11장에서 월별 다중탈퇴율을 산출할 때 바로 이 UDD류 가정이 실무적으로 활용된다.",
        "relatedFormulas": "II-9(단수부분에 대한 세 가지 표준 가정)의 첫 번째 사례.",
        "prerequisites": ["II-5 사력", "I-2 생명표"],
        "leadsTo": ["II-9 단수부분에 대한 가정", "11장 I-5~7 월별 다중탈퇴율 산출"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 11장(최신보험수리학) 월별 다중탈퇴율 산출"], "연 단위 생명표를 월 단위로 세분화하는 이 보간 논리가 IFRS17 월별 현금흐름 생성의 실무적 기초다."),
    },
    {
        "num": "II-9", "title": "단수부분에 대한 가정", "titleEn": "fractional age assumptions", "page": 171,
        "def": "정수년 사이(단수부분)의 생사확률을 다루는 세 가지 표준 가정 — UDD(균등분포), 지수가정(사력 일정), 발라주가정(Balducci, 현가함수 선형).",
        "symbols": [sym("ₛqₓ", "x세인 사람이 s년(0<s<1) 내 사망할 확률"), sym("ₛpₓ", "x세인 사람이 s년 생존할 확률")],
        "assumptions": ["세 가정 모두 lₓ와 lₓ₊₁ 두 점만 주어졌을 때 그 사이를 보간하는 서로 다른 방법"],
        "formula": r"\text{UDD: } {}_sq_x = s\,q_x \qquad \text{지수가정: } \mu(x+s)=\text{상수} \qquad \text{Balducci: } \frac{1}{{}_sp_x} = 1+(1-s)q_x",
        "derivationSteps": [
            step("UDD는 lₓ₊ₛ=lₓ−s·dₓ(선형)를 가정하므로:", r"{}_sq_x = \frac{l_x - l_{x+s}}{l_x} = \frac{s\,d_x}{l_x} = s\,q_x"),
            step("지수가정(constant force)은 사력이 그 구간에서 상수라고 가정하므로 ₛpₓ=exp(−sμ)=(pₓ)ˢ의 형태를 준다(II-7 이용).", None),
            step("Balducci 가정은 '현가함수(1/ₛpₓ)가 s에 대해 선형'이라고 가정하는 방식으로, 세 가정 중 실무에서 가장 덜 쓰이지만 이론적으로 대비된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "세 가정 중 실무 계산 편의상 UDD가 가장 널리 쓰인다. 세 가정 모두 정수년 경계값(lₓ, lₓ₊₁)은 동일하게 재현하지만, 그 사이 곡선의 모양(볼록/오목/선형)만 다르게 가정한다는 점을 이해하는 것이 핵심이다.",
        "relatedFormulas": "II-8의 UDD 근사식과 동일한 논리의 일반화.",
        "prerequisites": ["II-5 사력", "II-8 사력과 평균여명의 근사치"],
        "leadsTo": ["3장 II-4 보험금 사망즉시급과 연말급의 관계"],
        "ifrs17": ifrs("간접적 연관", note="단수부분 가정 자체가 해설서에서 다뤄지지는 않지만, 월별·일별 현금흐름을 산출하는 실무 계산의 배경이 된다."),
    },
    {
        "num": "II-10", "title": "사망법칙", "titleEn": "analytic laws of mortality", "page": 177,
        "def": "생명표 전체를 몇 개의 모수로 표현하는 해석적 사망법칙(analytic law of mortality). 대표적으로 드무아브르(De Moivre, 균등분포), 곰페르츠(Gompertz), 메이컴(Makeham) 법칙이 있다.",
        "symbols": [sym("ω", "드무아브르 법칙에서의 한계연령"), sym("B, c", "곰페르츠 법칙의 모수(B>0, c>1)"), sym("A", "메이컴 법칙에서 추가되는 나이무관 상수 사망위험")],
        "assumptions": ["각 법칙은 실제 생명표를 특정 함수형태로 근사하기 위한 모형화 가정"],
        "formula": r"\text{De Moivre: } S(x)=1-\frac{x}{\omega} \qquad \text{Gompertz: } \mu(x)=Bc^x \qquad \text{Makeham: } \mu(x)=A+Bc^x",
        "derivationSteps": [
            step("곰페르츠 법칙은 '사력이 나이에 따라 지수적으로 증가한다'는 경험적 관찰(노화에 따른 사망위험 가속)을 μ(x)=Bcˣ (c>1)로 모형화한 것이다.", None),
            step("메이컴은 여기에 나이와 무관한 상수 사망위험(사고사 등) A를 더해 현실 데이터에 더 잘 맞도록 확장한다:", r"\mu(x) = A + Bc^x"),
            step("드무아브르 법칙은 사력 대신 생존함수를 직접 선형으로 가정한다(0세부터 ω세까지 균등하게 사망):", r"S(x) = 1-\frac{x}{\omega}, \quad 0\le x\le \omega"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "실제 사망률 데이터는 표(lₓ)로만 존재하지만, 이를 몇 개의 숫자(모수)로 요약할 수 있다면 계산과 분석이 훨씬 쉬워진다. 곰페르츠·메이컴 법칙은 실제 인간 사망률의 '노화 가속' 패턴을 잘 근사하는 것으로 알려져 있다.",
        "relatedFormulas": "II-5 사력의 구체적 함수형태 지정.",
        "prerequisites": ["II-5 사력"],
        "leadsTo": ["II-11 특수한 생존분포", "3장 II-6 특수한 생존분포와 생명보험"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="해석적 사망법칙은 실무 가격산출·모형검증에 참고되는 이론이지만 IFRS17은 특정 사망법칙을 규정하지 않고 '회사 고유의 최선추정'을 요구한다(4.4.5)."),
    },
    {
        "num": "II-11", "title": "특수한 생존분포", "page": 179,
        "def": "와이블분포 등 사력이 나이의 거듭제곱으로 증가하는 분포를 비롯한 여러 이론적 생존분포 모형.",
        "symbols": [sym("k", "와이블분포의 척도모수"), sym("n", "와이블분포의 형태모수")],
        "assumptions": ["곰페르츠의 지수적 증가 대신 거듭제곱 형태로 사력 증가를 모형화"],
        "formula": r"\mu(x) = k\,x^{n-1} \quad (\text{Weibull})",
        "derivationSteps": [
            step("곰페르츠 μ(x)=Bcˣ가 지수함수 형태로 사력이 증가한다고 가정했다면, 와이블분포는 거듭제곱 형태로 증가한다고 가정해 더 유연하게 데이터에 적합시킬 수 있도록 일반화한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-10의 사망법칙들을 더 넓은 함수족으로 일반화한 것으로, 실무보다는 이론적 완결성을 위해 다뤄지는 절이다.",
        "relatedFormulas": "II-10 사망법칙의 일반화.",
        "prerequisites": ["II-10 사망법칙"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
]

data_ch2 = {
    "num": 2, "title": "생존분포와 생명표",
    "summary": "사망률·탈퇴율을 확률적으로 다루는 장. 생존함수 S(x), 사력 μ(x), 생명표 lₓ가 이후 3~12장 전체 계산의 확률적 기반이 된다. IFRS17의 미래현금흐름 추정(사망률·해지율 등 비금융가정)과 위험조정(RA)이 이 확률분포를 전제로 계산된다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 2:
        data["chapters"][i] = data_ch2
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 2 upgraded to full schema:", len(I) + len(II), "items")
