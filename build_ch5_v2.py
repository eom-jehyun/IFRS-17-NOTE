# -*- coding: utf-8 -*-
# 제5장 순보험료 — 12-field schema.
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
        "num": "I-1", "title": "연납평준순보험료", "titleEn": "level annual net premium", "page": 380,
        "def": "수지상등의 원칙(보험자가 받는 보험료의 현가 = 보험자가 지급할 급부의 현가)에 따라, 매년 동일한 금액으로 정해지는 순보험료(사업비 제외, 급부 원가만 반영). 수학적으로는 두 APV(3장 급부현가, 4장 보험료현가)를 같다고 놓고 미지수(보험료 P)를 구하는 방정식이고, 보험수리학적으로는 보험료 산정의 가장 기본적인 원리다.",
        "symbols": [sym("P", "연납평준순보험료(연 1회 납입, 매년 동일액)"), sym("Ax", "종신보험 급부현가율(3장 I-3)"), sym("äx", "종신연금 보험료현가율(4장 I-1)")],
        "assumptions": ["보험료는 매년 초, 생존시에만 납입(사망하면 납입 중단)", "종신보험(사망시 1 지급) 기준"],
        "formula": r"P \cdot \ddot a_x = A_x \;\Longrightarrow\; P = \frac{A_x}{\ddot a_x}",
        "derivationSteps": [
            step("수지상등의 원칙: '보험자가 받을 것으로 기대하는 보험료의 현가'와 '지급할 것으로 기대하는 급부의 현가'가 같아야 한다.", None),
            step("보험료는 생존해 있는 동안 매년 P씩 납입되므로 그 현가는 P·äx(4장 I-1)이고, 급부는 사망시 1을 지급하므로 그 현가는 Ax(3장 I-3)이다. 두 현가를 같다고 놓으면:", r"P\cdot \ddot a_x = A_x"),
            step("이를 P에 대해 풀면:", r"P = \frac{A_x}{\ddot a_x}"),
        ],
        "derivation": "",
        "termMeanings": [term("P·äx", "보험자가 받을 것으로 기대하는 보험료의 현가(수입측)"), term("Ax", "보험자가 지급할 것으로 기대하는 급부의 현가(지출측)")],
        "intuition": "이 식은 '보험자가 손해도 이익도 보지 않도록(순보험료 기준) 보험료를 정한다'는 의미다. 4장 I-9의 항등식 Ax=1−d·äx를 대입하면 P=1/äx−d로도 표현할 수 있어, äx만 알면 즉시 P를 구할 수 있다.",
        "relatedFormulas": "3장 I-3(Ax), 4장 I-1(äx), 4장 I-9(Ax=1−däx)가 모두 이 하나의 식으로 수렴한다.",
        "prerequisites": ["3장 I-3 사망보험", "4장 I-1 종신연금"],
        "leadsTo": ["I-2 연m회 분할납순보험료", "6장 계약자적립액"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4 현금흐름"], "'유입현금흐름의 현가 = 유출현금흐름의 현가'라는 균형 논리는 IFRS17 최선추정부채가 '유입-유출 현금흐름의 현재가치'로 정의되는 구조와 뿌리가 같다. 다만 IFRS17은 이 균형을 보험료 산정 목적이 아니라 매 결산시점 부채 재평가 목적으로 사용하며, 산식의 균형이 반드시 0이 되도록 강제하지 않는다(차액이 CSM 또는 손실요소가 됨)."),
    },
    {
        "num": "I-2", "title": "연m회 분할납순보험료", "page": 389,
        "def": "연납보험료 P를 연 m회로 나눠 납입할 때의 보험료 P⁽ᵐ⁾.",
        "symbols": [sym("P⁽ᵐ⁾", "연 m회 분할납 시 1회당 보험료 관련 연간 총액"), sym("äx⁽ᵐ⁾", "연 m회 납입 생명연금 현가율(4장 I-8)")],
        "assumptions": ["분할납이라도 총 연간 납입액의 현가가 P·äx(I-1)와 같아야 함"],
        "formula": r"P^{(m)} \cdot \ddot a_x^{(m)} = A_x \;\Longrightarrow\; P^{(m)} = \frac{A_x}{\ddot a_x^{(m)}}",
        "derivationSteps": [
            step("I-1과 동일한 수지상등 원칙을, 보험료 납입주기만 연 m회로 바꿔 적용한다. 보험료 현가는 4장 I-8의 äx⁽ᵐ⁾를 사용한다:", r"P^{(m)}\cdot \ddot a_x^{(m)} = A_x"),
            step("이를 P⁽ᵐ⁾에 대해 풀면:", r"P^{(m)} = \frac{A_x}{\ddot a_x^{(m)}}"),
            step("4장 I-8에서 äx⁽ᵐ⁾<äx(m>1인 경우)였으므로, P⁽ᵐ⁾>P(=Ax/äx)가 된다 — 분할납이 연납보다 총액 기준으로 더 비싸다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "분할납이 더 비싼 이유는, 같은 총액이라도 더 잘게 나눠 늦게 걷으면 보험자 입장에서 그만큼 자금을 늦게 받아 이자 손실이 생기기 때문이다.",
        "relatedFormulas": "I-1의 분할납 버전, 4장 I-8 äx⁽ᵐ⁾ 재사용.",
        "prerequisites": ["I-1 연납평준순보험료", "4장 I-8 연m회 지급하는 경우의 생명연금"],
        "leadsTo": ["I-3 보험료 반환부 보험"],
        "ifrs17": ifrs("간접적 연관", note="분할납 보험료의 현가 계산은 IFRS17 유입현금흐름 추정시 실제 납입주기를 반영해야 한다는 원칙(4.4)과 통하지만 이 공식 자체가 조문화되어 있지는 않다."),
    },
    {
        "num": "I-3", "title": "보험료 반환부 보험", "titleEn": "return of premium insurance", "page": 395,
        "def": "사망시 보험금뿐 아니라 그때까지 납입한 보험료를 (이자 포함 또는 원금만) 함께 반환하는 특약이 있는 보험.",
        "symbols": [sym("P'", "보험료반환부 보험의 순보험료"), sym("(IA)¹x:n|", "사망시점까지 납입한 보험료 누계에 비례해 증가하는 급부의 APV(1장 I-8 누가연금 구조와 유사)")],
        "assumptions": ["사망시 '기본보험금 + 그때까지 납입한 보험료(누계)'를 지급"],
        "formula": r"P' \cdot \ddot a_{x:\overline{n}|} = A^{\;1}_{x:\overline{n}|} + P' \cdot (I A)^{\;1}_{x:\overline{n}|}",
        "derivationSteps": [
            step("급부가 두 부분으로 구성된다 — 기본 사망보험금(정기보험 A¹x:n|)과, 사망시점까지 낸 보험료 누계(P'×사망시점까지의 납입횟수, 이는 1장 I-8의 누가연금과 유사한 구조로 APV화된다).", None),
            step("수지상등 원칙(보험료 현가 = 급부 현가)을 세우면 P'가 방정식의 양변에 모두 나타난다(급부 자체가 P'에 비례하므로):", r"P'\ddot a_{x:\overline n|} = A^{\;1}_{x:\overline n|} + P'\cdot (IA)^{\;1}_{x:\overline n|}"),
            step("P'에 대해 정리하면:", r"P' = \frac{A^{\;1}_{x:\overline n|}}{\ddot a_{x:\overline n|} - (IA)^{\;1}_{x:\overline n|}}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "이런 유형의 문제는 '구하려는 미지수(P')가 급부 쪽에도 등장'하는 것이 특징이며, 이 경우 단순 나눗셈이 아니라 P'를 양변에서 정리하는 대수적 절차가 한 단계 더 필요하다.",
        "relatedFormulas": "1장 I-8 누가연금 구조의 응용.",
        "prerequisites": ["I-1 연납평준순보험료", "1장 I-8 변동연금"],
        "leadsTo": ["II-7 보험료 반환부 정기보험과 생사혼합보험의 보험료"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
]

II = [
    {
        "num": "II-1", "title": "보험료계산의 원칙", "page": 403,
        "def": "I파트에서 다룬 수지상등의 원칙을 확률변수 관점에서 엄밀하게 재정의한다 — '손실(Loss)'이라는 확률변수 L을 정의하고, 순보험료는 E[L]=0이 되도록 정하는 값임을 보인다.",
        "symbols": [sym("L", "보험자의 손실(확률변수)"), sym("K(x)", "미래개산생존기간(2장 II-4)")],
        "assumptions": ["종신보험, 연납평준순보험료 기준"],
        "formula": r"L = v^{K(x)+1} - P\cdot \ddot a_{\overline{K(x)+1}|}, \qquad E[L]=0",
        "derivationSteps": [
            step("보험자의 손실 L은 '실제 지급한 급부의 현가'에서 '실제 받은 보험료의 현가'를 뺀 값으로 정의된다. 두 값 모두 사망시점 K(x)에 의존하는 확률변수다:", r"L = v^{K(x)+1} - P\cdot \ddot a_{\overline{K(x)+1}|}"),
            step("순보험료 P는 '평균적으로 손해도 이익도 없다'는 원칙, 즉 E[L]=0이 되도록 정해진다. E[L]=0을 풀면 E[v^(K(x)+1)]=P·E[ä‾(K(x)+1)|]이 되고, 이는 I-1의 Ax=P·äx와 정확히 같은 식이다.", r"E[L] = A_x - P\ddot a_x = 0 \;\Longrightarrow\; P=\frac{A_x}{\ddot a_x}"),
        ],
        "derivation": "",
        "termMeanings": [term("L", "특정 사망시나리오 하에서 보험자가 실제로 보는 손익(+면 손실, −면 이익)"), term("E[L]=0", "모든 시나리오에 대해 평균을 내면 손익이 0이 되도록 보험료를 정한다는 조건")],
        "intuition": "I-1에서는 '현가의 균형'으로 보험료를 정의했지만, 여기서는 '확률변수 L의 기대값이 0'이라는 더 엄밀한 통계적 정의를 사용한다. 이 관점은 7장(영업보험료)에서 Var(L)(손실의 분산, 즉 리스크)을 분석할 때 필수적이다.",
        "relatedFormulas": "I-1의 확률변수 버전.",
        "prerequisites": ["I-1 연납평준순보험료", "2장 II-4 (x)의 미래개산생존기간"],
        "leadsTo": ["7장 II-3 미래손실의 분산"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="손실 확률변수 L 자체는 순보험료 산정이론이며, IFRS17의 손실요소(loss component)는 계약집합 최초인식 시점의 기대 손익(양/음)을 가리키는 회계개념으로 정의가 다르다."),
    },
    {
        "num": "II-2", "title": "연납평준순보험료 (일반이론)", "page": 404,
        "def": "다양한 급부구조(정기보험, 생사혼합보험 등)에 대해 I-1의 원칙을 체계적으로 적용하는 절.",
        "symbols": [sym("P(Ax)", "종신보험 순보험료를 나타내는 일반 표기법(급부 종류를 괄호 안에 표기)")],
        "assumptions": ["각 급부구조에 맞는 APV(3장) 사용"],
        "formula": r"P(\text{급부}) = \frac{APV(\text{급부})}{\ddot a_x \text{ 또는 } \ddot a_{x:\overline n|}}",
        "derivationSteps": [
            step("I-1의 원칙(P·(보험료연금현가율) = 급부현가)을 정기보험, 생사혼합보험 등 어떤 급부구조에도 동일하게 적용할 수 있다는 일반화다 — 분자만 해당 상품의 APV로 바꾸면 된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-1이 종신보험이라는 특수사례를 다뤘다면, 이 절은 '급부가 무엇이든 분자에 그 APV를 넣으면 된다'는 일반 절차를 확립한다.",
        "relatedFormulas": "I-1의 일반화.",
        "prerequisites": ["I-1 연납평준순보험료", "3장 I-4 생사혼합보험"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-3", "title": "연m회 분할납 진보험료(평준인 경우)", "page": 416,
        "def": "I-2를 일반이론 관점(확률변수 L)에서 재정리.",
        "symbols": [],
        "assumptions": [],
        "formula": r"E[L^{(m)}]=0 \;\Longrightarrow\; P^{(m)} = \frac{A_x}{\ddot a_x^{(m)}}",
        "derivationSteps": [
            step("II-1의 손실 확률변수 정의를 분할납 보험료 구조에 맞게 재구성하고, E[L⁽ᵐ⁾]=0 조건에서 I-2와 동일한 결과를 다시 유도한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-2의 확률변수 버전.",
        "relatedFormulas": "I-2, II-1의 결합.",
        "prerequisites": ["I-2 연m회 분할납순보험료", "II-1 보험료계산의 원칙"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-4", "title": "연속납순보험료", "titleEn": "continuous premium", "page": 419,
        "def": "보험료를 매 순간 연속적으로(예: 매일 조금씩) 납입한다고 가정한 극한 형태.",
        "symbols": [sym("P̄", "연속납순보험료율"), sym("āx", "연속생명연금 현가율(4장 II-3)"), sym("Āx", "사망즉시급 현가율(3장 II-3)")],
        "assumptions": ["급부는 사망즉시급, 보험료는 연속납"],
        "formula": r"\bar P \cdot \bar a_x = \bar A_x \;\Longrightarrow\; \bar P = \frac{\bar A_x}{\bar a_x}",
        "derivationSteps": [
            step("I-1의 수지상등 원칙을 두 축(급부·보험료) 모두 연속형으로 바꿔 적용한다 — 급부현가는 Āx(3장 II-3), 보험료현가는 āx(4장 II-3):", r"\bar P \cdot \bar a_x = \bar A_x"),
            step("이를 P̄에 대해 풀면:", r"\bar P = \frac{\bar A_x}{\bar a_x}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "실무에서는 쓰이지 않는 이론적 극한이지만, 이산형 근사식(II-3 등)의 정확한 기준점 역할을 한다.",
        "relatedFormulas": "I-1의 완전 연속형 버전.",
        "prerequisites": ["3장 II-3 보험금 사망즉시급", "4장 II-3 연속생명연금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-5", "title": "분할부납 보험료", "page": 428,
        "def": "II-3(평준 분할납)을 넘어, 매 분할 회차마다 금액이 다를 수 있는 일반적인 분할납 구조.",
        "symbols": [],
        "assumptions": ["1장 II-3(일반 변동연금)의 임의 지급액 구조를 보험료 납입에 응용"],
        "formula": r"\sum_j P_j \cdot v^{t_j}\cdot {}_{t_j}p_x = APV(\text{급부})",
        "derivationSteps": [
            step("1장 II-3의 일반 변동연금 PV=Σbₖvᵏ 구조를, '생존시에만 납입'이라는 조건을 추가해 보험료 납입흐름에 적용한다.", r"\sum_j P_j v^{t_j}\cdot {}_{t_j}p_x = APV(\text{급부})"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "II-2가 '급부의 일반화'였다면 이 절은 '보험료 납입구조의 일반화'다.",
        "relatedFormulas": "1장 II-3의 응용.",
        "prerequisites": ["1장 II-3 일반적인 변동연금", "II-2 연납평준순보험료"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-6", "title": "미사용보험료 반환부 보험", "page": 430,
        "def": "만기 전 해지 등으로 '앞으로 낼 필요가 없어진 보험료' 상당분을 돌려주는 특약.",
        "symbols": [],
        "assumptions": [],
        "formula": r"\text{환급액} \approx (\text{잔여 계약기간의 보험료 현가 상당분})",
        "derivationSteps": [
            step("아직 발생하지 않은 미래 보험료 납입의무가 사라진 만큼, 그에 상응하는 가치를 돌려준다는 대칭적 논리다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "6장의 해약환급금 개념과 유사한 논리 구조(계약이 조기 종료될 때 정산이 필요하다는 발상)를 보험료 쪽에 적용한 것이다.",
        "relatedFormulas": "6장 I-3 해약환급금과 개념적으로 유사.",
        "prerequisites": ["I-1 연납평준순보험료"],
        "leadsTo": ["6장 I-3 해약환급금"],
        "ifrs17": ifrs("간접적 연관", note="계약 조기종료시 정산 논리는 IFRS17 해지환급금·투자요소 처리와 개념적으로 유사하나 이 항목 자체가 특정 조문과 대응되지는 않는다."),
    },
    {
        "num": "II-7", "title": "보험료 반환부 정기보험과 생사혼합보험의 보험료", "page": 436,
        "def": "I-3(종신보험 기준)을 정기보험·생사혼합보험에 확장 적용.",
        "symbols": [],
        "assumptions": [],
        "formula": r"P' \cdot \ddot a_{x:\overline n|} = APV(\text{기본급부}) + P'\cdot (IA)_{x:\overline n|}",
        "derivationSteps": [
            step("I-3와 동일한 절차(P'가 급부 쪽에도 나타나므로 정리 필요)를, 정기보험·생사혼합보험이라는 다른 급부구조에 반복 적용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-3의 확장.",
        "relatedFormulas": "I-3의 확장.",
        "prerequisites": ["I-3 보험료 반환부 보험", "3장 I-4 생사혼합보험"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-8", "title": "특수한 생존분포와 평준순보험료", "page": 445,
        "def": "드무아브르 법칙 등 특수 생존분포 하에서 P가 닫힌 형태로 정리되는 경우들.",
        "symbols": [],
        "assumptions": ["드무아브르 법칙(2장 II-10)"],
        "formula": r"P = \frac{A_x}{\ddot a_x} \;\; \text{에 3장 II-6, 4장 II-8의 닫힌 형태를 대입}",
        "derivationSteps": [
            step("3장 II-6에서 구한 드무아브르 법칙 하의 Ax와 4장 II-8에서 구한 äx를 I-1의 P=Ax/äx에 대입하면, 순보험료도 닫힌 형태로 정리된다.", None),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "3장·4장에서 이미 구해둔 특수 생존분포 결과를 재사용하는 응용절이다.",
        "relatedFormulas": "3장 II-6, 4장 II-8, I-1의 결합.",
        "prerequisites": ["I-1 연납평준순보험료", "3장 II-6 특수한 생존분포와 생명보험", "4장 II-8 특수한 생존분포와 생명연금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
]

data_ch5 = {
    "num": 5, "title": "순보험료",
    "summary": "수지상등원칙에 의한 순보험료 산출. 3장(급부현가)과 4장(연금현가)을 결합해 실제 보험료를 계산하는 장이다. IFRS17 회계모형에서는 보험료 자체보다 '계약자로부터 받을 것으로 예상되는 보험료 현금흐름'이 이행현금흐름의 유입 측 요소로 다뤄진다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 5:
        data["chapters"][i] = data_ch5
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 5 upgraded:", len(I) + len(II), "items")
