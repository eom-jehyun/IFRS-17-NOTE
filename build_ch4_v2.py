# -*- coding: utf-8 -*-
# 제4장 생명연금 — 12-field schema, 전수검사 기준 적용.
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
        "num": "I-1", "title": "종신연금", "titleEn": "whole life annuity-due", "page": 268,
        "def": "생존해 있는 한 매년 초(기시급) 1씩 평생 지급하는 연금. 수학적으로는 3장 Ax와 마찬가지로 확률가중 현가의 합이지만 급부가 '생존시에만' 지급된다는 점이 3장(사망시 지급)과 대비되고, 보험수리학적으로는 연금보험·종신형 저축상품의 핵심 계산도구다.",
        "symbols": [sym("äx", "x세 기시급 종신연금의 현가율"), sym("v", "할인인자(1장 I-3)"), sym("ₖpₓ", "k년 생존확률(2장 I-3)")],
        "assumptions": ["매년 초(0,1,2,…시점) 생존해 있으면 1 지급", "평생(종신) 지급"],
        "formula": r"\ddot a_x = \sum_{k=0}^{\infty} v^k \cdot {}_kp_x",
        "derivationSteps": [
            step("k시점(매년 초)에 지급받는 1을 받으려면 그때까지 생존(확률 ₖpₓ)해야 한다.", None),
            step("3장 I-1의 APV 정의(현가×확률의 합)를 이 급부구조에 적용하면:", r"\ddot a_x = \sum_{k=0}^{\infty} v^k\cdot {}_kp_x"),
            step("k=0항은 v⁰·₀pₓ=1(가입 즉시 생존이 확인된 상태이므로 첫 회는 반드시 지급)임에 유의한다.", None),
        ],
        "derivation": "",
        "termMeanings": [term("vᵏ", "k시점 1원의 현재가치"), term("ₖpₓ", "k시점까지 생존할 확률")],
        "intuition": "3장의 Ax가 '사망이라는 한 번의 사건'에 대한 현가라면, äx는 '매년 생존을 확인하며 반복 지급'되는 현가의 합이다. 두 값은 서로 무관하지 않고, I-9에서 밝혀지듯 엄밀한 항등식으로 연결되어 있다.",
        "relatedFormulas": "3장 I-1의 APV 정의를 급부구조만 바꿔 재적용. I-9에서 Ax와의 관계가 도출된다.",
        "prerequisites": ["1장 I-3 현가와 할인", "2장 I-3 생명확률", "3장 I-1 보험료계산의 기초"],
        "leadsTo": ["I-2 유기생명연금", "I-9 생명보험과 생명연금의 일시납순보험료의 관계"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "연금형 상품(생존시 반복 지급)의 미래현금흐름 추정이 이 구조를 그대로 사용한다."),
    },
    {
        "num": "I-2", "title": "유기생명연금", "titleEn": "temporary life annuity-due", "page": 271,
        "def": "최대 n년까지만(생존하는 동안) 매년 초 1씩 지급하는 연금.",
        "symbols": [sym("äx:n|", "x세, n년 유기 기시급 생명연금의 현가율"), sym("n", "최대 지급연수")],
        "assumptions": ["k=0,…,n−1 시점에 생존해 있으면 1 지급(최대 n회)"],
        "formula": r"\ddot a_{x:\overline{n}|} = \sum_{k=0}^{n-1} v^k \cdot {}_kp_x",
        "derivationSteps": [
            step("I-1 종신연금의 무한합을 n항(k=0,…,n−1)에서 끊은 형태다 — n년째 이후의 생사와 무관하게 지급이 종료된다.", r"\ddot a_{x:\overline{n}|} = \sum_{k=0}^{n-1} v^k\cdot {}_kp_x"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "종신연금은 '평생', 유기연금은 '최대 n년'이라는 상한이 있다는 점만 다르다. 실무의 확정기간 연금보험(예: 10년 확정 생존연금)이 이 구조에 해당한다.",
        "relatedFormulas": "I-1의 유한합 버전.",
        "prerequisites": ["I-1 종신연금"],
        "leadsTo": ["I-3 거치연금"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.4 현금흐름"], "확정기간 연금상품의 미래현금흐름 추정에 직접 사용된다."),
    },
    {
        "num": "I-3", "title": "거치연금", "titleEn": "deferred annuity", "page": 272,
        "def": "가입 후 일정기간(거치기간 m년) 동안은 지급하지 않다가, m년 후부터 생존시 지급을 개시하는 연금.",
        "symbols": [sym("m|äx", "m년 거치 종신연금의 현가율"), sym("äx₊ₘ", "x+m세 기준 종신연금의 현가율")],
        "assumptions": ["0~m−1년차는 지급 없음", "m년째부터 생존시 매년 초 지급 개시"],
        "formula": r"{}_{m|}\ddot a_x = \ddot a_x - \ddot a_{x:\overline{m}|} = v^m \cdot {}_mp_x \cdot \ddot a_{x+m}",
        "derivationSteps": [
            step("[첫 번째 방법 — 차감법] 전체 종신연금(I-1)에서 거치기간 동안의 유기연금(I-2) 부분을 빼면, 거치기간 이후 부분만 남는다:", r"{}_{m|}\ddot a_x = \ddot a_x - \ddot a_{x:\overline{m}|}"),
            step("[두 번째 방법 — 직접법] 'm년 생존(확률 ₘpₓ, 그 시점까지 vᵐ 할인) 후, 그 시점 기준으로 종신연금 äx₊ₘ을 새로 시작'한다는 논리로도 유도된다:", r"{}_{m|}\ddot a_x = v^m \cdot {}_mp_x \cdot \ddot a_{x+m}"),
            step("두 방법이 항등식으로 일치함이 증명될 수 있다(등비급수의 재인덱싱).", None),
        ],
        "derivation": "",
        "termMeanings": [term("vᵐ·ₘpₓ", "m년 시점까지 생존해 도달할 확률과 그 현가"), term("äx₊ₘ", "그 시점 기준으로 다시 시작하는 종신연금")],
        "intuition": "같은 값을 구하는 두 가지 관점(전체에서 앞부분을 빼는 차감법, m년 후를 새 출발점으로 보는 직접법)이 있다는 것은 이후 여러 장에서 반복되는 유용한 패턴이다.",
        "relatedFormulas": "I-1, I-2의 조합.",
        "prerequisites": ["I-1 종신연금", "I-2 유기생명연금"],
        "leadsTo": ["I-4 보증기간부 생명연금"],
        "ifrs17": ifrs("간접적 연관", note="거치연금 구조 자체보다, IFRS17에서 특정 시점 이후 발생하는 미래현금흐름을 현가화하는 일반 논리와 연결된다."),
    },
    {
        "num": "I-4", "title": "보증기간부 생명연금", "titleEn": "guaranteed annuity", "page": 274,
        "def": "생사와 무관하게 최소 n년은 보증 지급하고, n년 이후는 생존시에만 지급하는 연금(사망해도 유족이 잔여 보증기간분을 받음).",
        "symbols": [sym("äx:n‾|", "n년 보증부 종신연금의 현가율"), sym("a‾n|", "n년 확정연금의 현가율(1장 I-6, 기말급 표기이나 여기선 보증부분의 구조를 나타냄)")],
        "assumptions": ["0~n년: 생사 무관 확정지급(보증)", "n년 이후: 생존시에만 지급"],
        "formula": r"\ddot a_{x:\overline{n}|}^{\;\;\overline{\phantom{n}}} = \ddot a_{\overline{n}|} + {}_{n|}\ddot a_x",
        "derivationSteps": [
            step("전체 급부를 두 구간으로 나눈다 — n년까지는 생사에 관계없이 지급되는 확정연금 부분, n년 이후는 생존시에만 지급되는 거치생명연금(I-3) 부분.", None),
            step("두 부분은 서로 겹치지 않는(시간 구간이 다른) 현금흐름이므로 단순히 더한다:", r"\ddot a_{x:\overline{n}|}^{\;\;\overline{\phantom{n}}} = \ddot a_{\overline{n}|} + {}_{n|}\ddot a_x"),
        ],
        "derivation": "",
        "termMeanings": [term("ä‾n|", "확정연금 부분(생사 무관)"), term("ₙ|äx", "거치생명연금 부분(생존조건부, I-3)")],
        "intuition": "두 위험(확정 지급의무 + 생존조건부 지급의무)을 겹치지 않게 나눠, 이미 아는 두 공식(1장의 확정연금 + I-3의 거치연금)의 합으로 처리한다는 점에서 3장 I-4(생사혼합보험)와 같은 분해 전략이다.",
        "relatedFormulas": "1장 I-6(확정연금) + I-3(거치연금)의 결합.",
        "prerequisites": ["1장 I-6 확정연금", "I-3 거치연금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-5", "title": "forborne annuity (지급유예연금)", "page": 275,
        "def": "지급 시기를 뒤로 미루되 그동안의 지급액에 이자를 부리해 나중에 한꺼번에(혹은 이후 연금으로) 지급하는 개념.",
        "symbols": [sym("k", "유예기간(년)")],
        "assumptions": ["미룬 지급액에 대해 이자율 i로 부리"],
        "formula": r"(\text{미룬 지급액의 종가}) = (\text{원래 지급액}) \times (1+i)^k",
        "derivationSteps": [
            step("당장 받을 돈을 늦게 받는 대신, 그 기간 동안의 이자를 보상받는다는 1장 I-1의 종가 개념을 연금 지급 시점 조정에 그대로 응용한다.", r"(\text{미룬 지급액의 종가}) = (\text{원래 지급액})\times(1+i)^k"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이 개념 자체는 새로운 확률구조가 아니라, 1장 이자론의 종가 계산을 연금 실무(지급 연기)에 적용한 사례다.",
        "relatedFormulas": "1장 I-1 단위종가함수의 응용.",
        "prerequisites": ["1장 I-1 단위종가함수"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-6", "title": "변동연금", "titleEn": "increasing life annuity", "page": 281,
        "def": "지급액이 매년 증가(또는 감소)하는 생명연금. 1장 I-8(확정 누가연금)의 생존확률 결합 버전.",
        "symbols": [sym("(Iä)x", "x세 누가생명연금의 현가율")],
        "assumptions": ["k시점 생존시 지급액이 k+1 (k=0,1,2,…)"],
        "formula": r"(I\ddot a)_x = \sum_{k=0}^{\infty} (k+1)\cdot v^k \cdot {}_kp_x",
        "derivationSteps": [
            step("1장 I-8의 확정 누가연금 Σ(k+1)vᵏ 구조에, 각 시점의 지급 여부를 결정하는 생존확률 ₖpₓ를 추가로 곱하면 자연스럽게 확장된다:", r"(I\ddot a)_x = \sum_{k=0}^{\infty} (k+1)v^k\cdot {}_kp_x"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "물가상승 등을 반영해 매년 지급액이 커지는 연금 상품(체증형 연금)의 이론적 근거다.",
        "relatedFormulas": "1장 I-8의 생존확률 결합 확장.",
        "prerequisites": ["1장 I-8 변동연금", "I-1 종신연금"],
        "leadsTo": [],
        "ifrs17": ifrs("간접적 연관", note="체증형 급부 설계에 참고되나 해설서 특정 조문과 직접 대응되지 않는다."),
    },
    {
        "num": "I-7", "title": "계산기수와 일반식", "page": 286,
        "def": "äx를 계산기수로 표현하는 도구. Nx = Σ Dy.",
        "symbols": [sym("Nx", "Dx의 누적합(x세 이상 전체)"), sym("Dx", "생존급부 계산기수(=vˣlₓ, 3장 I-6)")],
        "assumptions": ["연간 기시급 기준"],
        "formula": r"\ddot a_x = \frac{N_x}{D_x}, \qquad N_x = \sum_{y=x}^{\infty} D_y",
        "derivationSteps": [
            step("äx=Σvᵏₖpₓ에서 ₖpₓ=lₓ₊ₖ/lₓ(2장 I-3)를 대입하고 lₓ로 묶으면:", r"\ddot a_x = \frac{1}{l_x}\sum_{k=0}^{\infty} v^k l_{x+k}"),
            step("분자·분모에 vˣ를 곱해 각 항을 v^(x+k)l_(x+k)=D_(x+k) 형태로 맞추면:", r"\ddot a_x = \frac{1}{v^x l_x}\sum_{k=0}^{\infty} v^{x+k}l_{x+k} = \frac{\sum_{y=x}^\infty D_y}{D_x} = \frac{N_x}{D_x}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "3장 I-6과 완전히 같은 논리로 Ax=Mx/Dx를 유도했던 것처럼, äx=Nx/Dx도 같은 계산기수 체계 안에서 나온다.",
        "relatedFormulas": "3장 I-6 Ax=Mx/Dx와 짝을 이루는 계산기수 공식.",
        "prerequisites": ["I-1 종신연금", "3장 I-6 계산기수와 일반식"],
        "leadsTo": ["I-8 연m회 지급하는 경우의 생명연금"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "I-8", "title": "연m회 지급하는 경우의 생명연금", "page": 287,
        "def": "연 1회가 아니라 연 m회(예: 매월)로 분할 지급하는 생명연금.",
        "symbols": [sym("äx⁽ᵐ⁾", "연 m회 분할지급 생명연금의 현가율"), sym("m", "연간 지급횟수")],
        "assumptions": ["UDD 가정(생사 사건이 연중 균등분포한다고 근사)"],
        "formula": r"\ddot a_x^{(m)} \approx \ddot a_x - \frac{m-1}{2m}",
        "derivationSteps": [
            step("총 지급액은 동일하되 더 자주(연 m회) 나눠 받으므로, 평균적으로 더 일찍 받는 효과가 있어 현가가 약간 커진다.", None),
            step("그 보정폭이 근사적으로 (m−1)/(2m)이라는 상수항으로 표현된다(Woolhouse 근사의 1차항, 1장 I-4의 명목이율 환산 논리와 유사한 구조):", r"\ddot a_x^{(m)} \approx \ddot a_x - \frac{m-1}{2m}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "월납 연금이 연납 연금보다 조금 더 비싼(현가가 큰) 이유는, 같은 금액을 더 잘게 쪼개 더 자주 받을수록 평균 수령시점이 앞당겨지기 때문이다.",
        "relatedFormulas": "1장 I-4의 명목이율 근사와 유사한 원리. II-7 Woolhouse 근사에서 더 정밀하게 다룬다.",
        "prerequisites": ["I-1 종신연금", "2장 II-9 단수부분에 대한 가정"],
        "leadsTo": ["I-9 생명보험과 생명연금의 일시납순보험료의 관계", "II-7 전통적인 근사치"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4 현금흐름"], "월납·월지급 상품의 현금흐름을 연 단위 근사가 아니라 실제 지급주기대로 반영해야 한다는 요구와 맥이 닿아 있다."),
    },
    {
        "num": "I-9", "title": "생명보험과 생명연금의 일시납순보험료의 관계", "page": 295,
        "def": "Ax와 äx를 잇는 항등식 — 생명보험/생명연금 이론 전체에서 가장 자주 쓰이는 핵심 관계식.",
        "symbols": [sym("Ax", "종신보험 현가율(3장 I-3)"), sym("äx", "종신연금 현가율(I-1)"), sym("d", "실할인율(1장 I-3, d=i/(1+i))")],
        "assumptions": ["연말급 사망보험 · 기시급 생명연금 기준"],
        "formula": r"A_x = 1 - d\,\ddot a_x",
        "derivationSteps": [
            step("매년 초 1원씩 보험료로 걷어 이자 d만큼씩(1장 I-3의 실할인율) 계속 떼어 적립한다고 생각한다. 걷은 보험료의 총 현가는 äx이다.", None),
            step("만약 사망하지 않고 계속 생존한다면, 결국 걷은 원금 전부(=1)를 그대로 돌려준다고 볼 수 있다 — 즉 '걷은 보험료의 현가(äx)에서 매년 떼어간 이자(d·äx)를 뺀 나머지'가 원금 1이 되어야 한다는 회계적 등식이 성립한다:", r"\ddot a_x - d\,\ddot a_x = (\text{원금 1의 현가 상당분})"),
            step("이 '원금 1' 부분이 정확히 사망시점에 지급되는 보험금 1의 현가, 즉 Ax와 같음을 보일 수 있다(엄밀한 증명은 äx=Σvᵏₖpₓ와 Ax=Σvᵏ⁺¹ₖ|qₓ를 d=1−v 관계로 직접 대수적으로 연결하여 확인 가능):", r"A_x = 1-d\,\ddot a_x"),
        ],
        "derivation": "",
        "termMeanings": [term("d·äx", "매년 걷은 보험료 중 '이자로 지급되는' 부분의 현재가치 합"), term("1−d·äx", "이자 지급분을 제외한 원금 상당분의 현재가치 = 사망보험금의 현가")],
        "intuition": "이 항등식은 '생명보험 = 원금(1) − 이자수취권(d·äx)'이라는 재무적 재해석을 가능하게 한다. Ax와 äx를 따로따로 암기하지 않고, 하나를 알면 즉시 다른 하나를 구할 수 있다는 점에서 실무·시험 모두에서 가장 많이 활용되는 관계식이다.",
        "relatedFormulas": "1장 I-3의 d=1−v 관계가 이 항등식의 대수적 기반이다.",
        "prerequisites": ["1장 I-3 현가와 할인", "3장 I-3 사망보험", "I-1 종신연금"],
        "leadsTo": ["5장 순보험료(수지상등원칙)", "6장 계약자적립액"],
        "ifrs17": ifrs("간접적 연관", note="이 항등식 자체는 IFRS17에서 직접 활용되지 않지만(IFRS17은 BEL·RA·CSM을 별도 산출), 보험료와 급부의 현가가 서로 대수적으로 긴밀히 연결된다는 사고방식은 이행현금흐름 전체(유입-유출)를 통합적으로 다루는 논리와 통한다."),
    },
]

II = [
    {
        "num": "II-1", "title": "연1회 지급의 생명연금", "page": 303,
        "def": "I파트의 äx를 확률변수의 기대값으로 엄밀히 재정의: äx = E[ä‾(K(x)+1)|].",
        "symbols": [sym("K(x)", "미래개산생존기간(2장 II-4)"), sym("ä‾(K(x)+1)|", "K(x)+1회 지급되는 확정연금의 현가(확률변수)")],
        "assumptions": ["기시급"],
        "formula": r"\ddot a_x = E\!\left[\ddot a_{\overline{K(x)+1}|}\right]",
        "derivationSteps": [
            step("2장에서 정의한 K(x)를 이용하면, 실제 지급횟수는 K(x)+1회이다(0시점부터 K(x)시점까지 매년 초).", None),
            step("매 시나리오(K(x)=k)에서 지급되는 총 현가는 확정연금 현가 ä‾(k+1)|와 같으므로, 그 기대값이 äx와 정확히 일치함을 기대값의 선형성으로 보일 수 있다:", r"\ddot a_x = E\left[\ddot a_{\overline{K(x)+1}|}\right] = \sum_{k=0}^\infty \ddot a_{\overline{k+1}|}\cdot P(K(x)=k)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "3장 II-1에서 Ax를 확률변수 v^(K(x)+1)의 기대값으로 재정의했던 것과 완전히 같은 패턴이다.",
        "relatedFormulas": "I-1의 엄밀한 재정의. 3장 II-1과 대칭.",
        "prerequisites": ["I-1 종신연금", "2장 II-4 (x)의 미래개산생존기간"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "연m회 지급의 생명연금", "page": 317,
        "def": "I-8을 확률모형 관점에서 정밀하게 유도한다.",
        "symbols": [sym("äx⁽ᵐ⁾", "연 m회 지급 생명연금의 현가율"), sym("ₖ/ₘpₓ", "k/m년 생존확률")],
        "assumptions": ["1/m년마다 생존 확인 후 1/m씩 지급"],
        "formula": r"\ddot a_x^{(m)} = \frac{1}{m}\sum_{k=0}^{\infty} v^{k/m} \cdot {}_{k/m}p_x",
        "derivationSteps": [
            step("지급주기를 1/m년 단위로 잘게 쪼갠 뒤, 매 세부시점(k/m년)마다 생존확률과 할인계수를 곱해 합산하고, 1회당 지급액이 1/m임을 반영한다:", r"\ddot a_x^{(m)} = \frac{1}{m}\sum_{k=0}^{\infty} v^{k/m}\cdot {}_{k/m}p_x"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-8의 근사식이 실제로는 이 정밀식을 UDD 가정 하에 근사한 것임을 보여준다.",
        "relatedFormulas": "I-8 근사식의 엄밀한 기반.",
        "prerequisites": ["I-8 연m회 지급하는 경우의 생명연금"],
        "leadsTo": ["II-3 연속생명연금"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-3", "title": "연속생명연금", "titleEn": "continuous life annuity", "page": 328,
        "def": "지급이 매 순간 이루어지는 극한적 연금. 수학적으로는 1장 II-2(연속확정연금)의 생존확률 결합 버전이고, 3장 Āx(사망즉시급)와 함께 연속시간 모형의 짝을 이룬다.",
        "symbols": [sym("āx", "연속 생명연금의 현가율")],
        "assumptions": ["매 순간 생존해 있으면 그 순간 미소 지급"],
        "formula": r"\bar a_x = \int_0^{\infty} v^t \cdot {}_tp_x\, dt",
        "derivationSteps": [
            step("II-2에서 m→∞ 극한을 취하면 이산합이 적분으로 수렴한다:", r"\bar a_x = \lim_{m\to\infty} \ddot a_x^{(m)} = \int_0^\infty v^t\cdot {}_tp_x\,dt"),
            step("3장의 Āx=∫vᵗₜpₓμ(x+t)dt와 부분적분으로 연결되는 관계식(Āx=1−δāx, I-9의 연속형 버전)도 여기서 함께 성립한다.", r"\bar A_x = 1-\delta\,\bar a_x"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-9의 항등식 Ax=1−däx가 이산형이었다면, Āx=1−δāx는 그 연속형 버전이다 — d↔δ, äx↔āx로 정확히 대응된다.",
        "relatedFormulas": "1장 II-2 연속확정연금의 생존확률 결합. 3장 II-3 Āx와 짝.",
        "prerequisites": ["1장 II-2 연속확정연금", "3장 II-3 보험금 사망즉시급"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-4", "title": "계산기수", "page": 340,
        "def": "äx, äx:n|, m|äx 등을 계산기수(Dx, Nx)로 일괄 표현하는 공식 정리.",
        "symbols": [sym("Nx", "I-7에서 정의한 계산기수")],
        "assumptions": [],
        "formula": r"\ddot a_{x:\overline{n}|} = \frac{N_x-N_{x+n}}{D_x}, \qquad {}_{m|}\ddot a_x = \frac{N_{x+m}}{D_x}",
        "derivationSteps": [
            step("I-7에서 äx=Nx/Dx를 얻은 논리를, 유기연금(I-2)·거치연금(I-3)에도 그대로 적용해 합산 구간만 조정한 Nx의 차분으로 표현한다.", r"\ddot a_{x:\overline{n}|} = \frac{N_x - N_{x+n}}{D_x}, \qquad {}_{m|}\ddot a_x = \frac{N_{x+m}}{D_x}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "계산기수 체계의 장점은, 일단 Dx·Nx표만 있으면 유기·거치 등 어떤 변형이든 뺄셈·나눗셈만으로 즉시 구할 수 있다는 데 있다.",
        "relatedFormulas": "I-7의 확장.",
        "prerequisites": ["I-7 계산기수와 일반식", "I-2 유기생명연금", "I-3 거치연금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-5", "title": "재귀식(점화식)", "page": 347,
        "def": "äx를 äx₊₁로 표현하는 순환 관계식.",
        "symbols": [sym("äx", "x세 종신연금 현가율"), sym("pₓ", "1년 생존확률")],
        "assumptions": ["기시급"],
        "formula": r"\ddot a_x = 1 + v\,p_x\,\ddot a_{x+1}",
        "derivationSteps": [
            step("'x세인 사람'은 즉시(0시점) 1을 받는다(생존이 이미 확인된 상태이므로 확정).", None),
            step("1년 뒤 생존(확률 pₓ)하면, 그때부터는 'x+1세인 사람'과 같은 상황이 되어 1년 할인된 äx₊₁의 가치를 추가로 갖는다:", r"\ddot a_x = 1 + v\,p_x\,\ddot a_{x+1}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "3장 II-5의 Ax 재귀식과 완전히 같은 논리 패턴(조건부기대값의 법칙)이며, 첫 항이 v·qₓ(사망시 즉시지급) 대신 1(즉시 확정지급)이라는 점만 다르다.",
        "relatedFormulas": "3장 II-5 Ax 재귀식과 대칭.",
        "prerequisites": ["I-1 종신연금"],
        "leadsTo": ["6장 계약자적립액 재귀식"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.8 보험부채의 변동"], "3장 II-5와 같은 이유로 12장 BEL 변동분석의 롤포워드 구조와 개념적으로 연결된다."),
    },
    {
        "num": "II-6", "title": "단수기간지급연금(완전연금)과 단수기간반환연금", "page": 349,
        "def": "연금 수급자가 지급주기 도중에 사망했을 때, 그 단수기간분을 별도로 지급(완전연금, complete annuity)하거나 이미 받은 것에서 환급(반환연금, apportionable annuity)하는 실무적 변형.",
        "symbols": [sym("α, β", "Woolhouse류 보정공식에서 쓰이는 근사계수(II-7 참고)")],
        "assumptions": ["UDD 가정 하에서 사망시점이 그 해 안에 균등분포"],
        "formula": r"\text{완전연금 현가} \approx \ddot a_x + (\text{단수기간 보정}), \quad \text{반환연금 현가} \approx \ddot a_x - (\text{단수기간 보정})",
        "derivationSteps": [
            step("UDD 가정 하에서 사망시점이 그 해 안에 균등분포한다는 성질을 이용해, 평균적으로 발생하는 단수기간분의 기대가치를 äx에 더하거나 빼는 보정항으로 유도한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "실무 연금상품은 '한 해가 다 지나야 정산'하는 대신, 사망 시점까지 일할 계산해 지급하거나(완전연금) 초과분을 환수하는(반환연금) 방식을 쓰는 경우가 많아 이런 보정이 필요하다.",
        "relatedFormulas": "II-7 Woolhouse 근사와 함께 실무적 보정 체계를 이룬다.",
        "prerequisites": ["2장 II-9 단수부분에 대한 가정", "I-1 종신연금"],
        "leadsTo": ["II-7 전통적인 근사치"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-7", "title": "전통적인 근사치", "titleEn": "Woolhouse's formula", "page": 359,
        "def": "우드하우스(Woolhouse) 공식 등, 정밀 계산(II-2) 없이도 äx⁽ᵐ⁾을 äx로부터 빠르게 근사하는 전통적 방법.",
        "symbols": [sym("äx⁽ᵐ⁾", "연 m회 지급 생명연금 현가율"), sym("δ", "이력(1장 I-5)"), sym("μₓ", "x세의 사력(2장 II-5)")],
        "assumptions": ["Euler-Maclaurin 급수전개가 유효할 정도로 매끄러운 함수"],
        "formula": r"\ddot a_x^{(m)} \approx \ddot a_x - \frac{m-1}{2m} - \frac{m^2-1}{12m^2}(\delta+\mu_x)",
        "derivationSteps": [
            step("Euler-Maclaurin 급수 전개를 이용하면, 연속함수의 적분(또는 세밀한 합)을 성긴 구간의 합(äx)과 그 도함수 보정항들로 근사할 수 있다.", None),
            step("이 근사를 사력·이력에 적용하면 I-8의 1차 근사(−（m−1)/(2m))에 2차 보정항(−（m²−1)/(12m²)(δ+μₓ))이 추가된 3항 근사식을 얻는다:", r"\ddot a_x^{(m)} \approx \ddot a_x - \frac{m-1}{2m} - \frac{m^2-1}{12m^2}(\delta+\mu_x)"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-8의 단순 근사보다 훨씬 정확하지만, 사력 μₓ이라는 추가 정보가 필요하다는 트레이드오프가 있다.",
        "relatedFormulas": "I-8의 정밀화 버전.",
        "prerequisites": ["I-8 연m회 지급하는 경우의 생명연금", "2장 II-5 사력"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-8", "title": "특수한 생존분포와 생명연금", "page": 365,
        "def": "드무아브르 법칙 등 특수 생존분포 하에서 äx가 닫힌 형태로 정리되는 경우들.",
        "symbols": [sym("ω", "드무아브르 법칙의 한계연령")],
        "assumptions": ["드무아브르 법칙: S(x)=1−x/ω"],
        "formula": r"\ddot a_x = \ddot a_{\overline{\omega-x}|} \quad (\text{드무아브르 법칙})",
        "derivationSteps": [
            step("드무아브르 법칙 하에서 생존확률 ₖpₓ=(ω−x−k)/(ω−x)는 등차수열이 되어, äx의 합이 3장 II-6과 같은 논리로 표준 확정연금 현가식과 같은 닫힌 형태로 축약된다.", r"\ddot a_x = \ddot a_{\overline{\omega-x}|}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "3장 II-6과 정확히 같은 패턴 — 균등분포라는 강한 가정을 두면 생명연금 공식이 이자론의 확정연금 공식으로 환원된다.",
        "relatedFormulas": "3장 II-6과 대칭 구조.",
        "prerequisites": ["2장 II-10 사망법칙", "3장 II-6 특수한 생존분포와 생명보험"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
]

data_ch4 = {
    "num": 4, "title": "생명연금",
    "summary": "연금형 급부(생존시 정기 지급)의 APV 계산. 3장(생명보험)과 짝을 이루는 장으로, Ax=1−däx(I-9)라는 핵심 항등식으로 두 장이 연결된다. 연금보험·저축성보험의 해약환급금·투자요소 관련 현금흐름 추정과 이어진다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 4:
        data["chapters"][i] = data_ch4
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 4 upgraded:", len(I) + len(II), "items")
