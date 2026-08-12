# -*- coding: utf-8 -*-
# 제1장 이자론 — 전수검사 반영판.
# 수정사항: (1) 모든 기호 누락 없이 정의 (2) 도출과정을 단계별 수식(derivationSteps)으로 전개
# (3) "항상/반드시" 등 절대표현에 조건 명시 (4) IFRS17 "다루지 않는다" 류 단정 표현을 완화
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
        "num": "I-1", "title": "단위종가함수", "titleEn": "accumulation function", "page": 2,
        "def": "원금 1을 t시점까지 투자했을 때의 종가(원리합계)를 나타내는 함수 a(t). 수학적으로는 a(0)=1인 증가함수이며, 보험수리학적으로는 이후 등장하는 모든 현재가치·기대현가 계산에서 '화폐의 시간가치'를 반영하는 가장 기초적인 도구다.",
        "symbols": [sym("a(t)", "t시점의 종가(단위원금 1 기준)"), sym("i", "연간 실이율(effective rate of interest)"), sym("t", "경과기간(년, 정수 또는 실수)")],
        "assumptions": ["원금 1을 t=0 시점에 투자", "복리: 매 기간 말 발생한 이자가 원금에 재투자(전입)됨", "단리: 매 기간 이자는 항상 최초 원금 1에 대해서만 계산됨(재투자 없음)"],
        "formula": r"a(t) = (1+i)^t \quad \text{(복리)} \qquad a(t) = 1 + it \quad \text{(단리)}",
        "derivationSteps": [
            step("복리는 '매 기간 말 이자가 원금에 재투자된다'는 정의에서 출발한다. 1기 후 종가는:", r"a(1) = 1+i"),
            step("2기 후에는 1기 후의 금액 (1+i) 전체에 다시 이율 i가 적용되므로:", r"a(2) = (1+i)(1+i) = (1+i)^2"),
            step("이를 t기까지 귀납적으로 반복하면:", r"a(t) = (1+i)^t"),
            step("단리는 반대로 '매 기간 원금 1에 대해서만' 이자 i가 붙으므로, t기간 누적이자는 단순히 i를 t번 더한 것이다:", r"a(t) = 1 + \underbrace{i+i+\cdots+i}_{t\text{번}} = 1+it"),
        ],
        "derivation": "",
        "termMeanings": [term("(1+i)", "한 기간 동안의 종가배율(복리)"), term("it", "단리에서 t기간 동안 누적된 총 이자")],
        "intuition": "복리는 '이자가 이자를 낳는' 구조이므로 시간이 지날수록 증가속도가 빨라지고(지수적 증가), 단리는 매 기간 같은 크기만큼만 늘어난다(선형 증가). t=1일 때는 두 식이 정확히 같은 값(1+i)을 주지만, t>1이면 복리 쪽이 항상 더 크다(i>0인 경우).",
        "relatedFormulas": "a(t)의 역수는 할인함수 a⁻¹(t) (I-3), a(t)의 순간증가율은 이력 δ (I-5)로 이어진다.",
        "prerequisites": [],
        "leadsTo": ["I-2 단리와 복리(실이율)", "I-3 현가와 할인"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 4.5 할인율"], "화폐의 시간가치 개념 자체가 IFRS17 보험부채 할인의 수학적 출발점이다."),
    },
    {
        "num": "I-2", "title": "단리와 복리 (실이율)", "titleEn": "effective rate of interest", "page": 5,
        "def": "n번째 해에 실제로 발생한 이자를 그 해 초의 금액으로 나눈 비율. 수학적으로는 a(t)의 이산 증가율이고, 보험수리학적으로는 '해마다 달라질 수 있는 실질 수익률'을 측정해 단리·복리의 성질을 비교하는 도구다.",
        "symbols": [sym("iₙ", "n번째 해의 실이율"), sym("a(n)", "n시점의 종가"), sym("a(n−1)", "n−1시점의 종가")],
        "assumptions": ["a(t)가 I-1에서 정의된 단위종가함수(단리 또는 복리)"],
        "formula": r"i_n = \frac{a(n)-a(n-1)}{a(n-1)}",
        "derivationSteps": [
            step("정의상 iₙ은 'n번째 해 초 금액 대비 n번째 해에 번 이자의 비율'이므로:", r"i_n = \frac{a(n)-a(n-1)}{a(n-1)}"),
            step("단리 a(t)=1+it를 대입하면:", r"i_n = \frac{[1+in]-[1+i(n-1)]}{1+i(n-1)} = \frac{i}{1+i(n-1)}"),
            step("이 식은 n이 커질수록 분모가 커지므로 iₙ이 점차 감소함을 보여준다. 복리 a(t)=(1+i)ᵗ를 대입하면:", r"i_n = \frac{(1+i)^n-(1+i)^{n-1}}{(1+i)^{n-1}} = (1+i)-1 = i"),
        ],
        "derivation": "",
        "termMeanings": [term("iₙ (단리)", "매년 감소 — 원금은 그대로인데 분모(누적액)만 커지기 때문"), term("iₙ (복리)", "매년 일정(=i) — 분자·분모가 같은 비율로 커지기 때문")],
        "intuition": "단리는 번 이자가 재투자되지 않으므로, 이미 불어난 원리금 대비 새로 버는 이자의 비중이 해가 갈수록 상대적으로 작아진다. 복리는 항상 같은 비율로 불어나므로 실이율이 i로 고정된다.",
        "relatedFormulas": "I-1의 두 종가함수(단리/복리)를 실이율 관점에서 재해석한 것.",
        "prerequisites": ["I-1 단위종가함수"],
        "leadsTo": ["I-4 명목이율과 명목할인율"],
        "ifrs17": ifrs("간접적 연관", note="해설서에서 이 항등식 자체를 다루지는 않지만, '이자율이 매기 달라질 수 있다'는 발상은 4.5 할인율의 기간구조(term structure) 개념과 이어진다."),
    },
    {
        "num": "I-3", "title": "현가와 할인", "titleEn": "present value and discount", "page": 8,
        "def": "미래 시점의 금액을 현재가치로 환산하는 할인인자 v와 할인함수 a⁻¹(t)=vᵗ, 그리고 이와 짝을 이루는 실할인율 d를 정의한다. 수학적으로는 종가함수 a(t)의 역함수이고, 보험수리학적으로는 이후 등장하는 모든 확정연금·생명보험·생명연금의 기대현재가치 계산의 기초가 된다.",
        "symbols": [sym("v", "할인인자(discount factor) — 1년 후 1원의 현재가치"), sym("a⁻¹(t)", "할인함수 — t시점 1원의 현재가치"), sym("d", "실할인율(rate of discount)"), sym("i", "연간 실이율")],
        "assumptions": ["복리 가정(연간 실이율 i로 매기 동일하게 부리)"],
        "formula": r"v = \frac{1}{1+i}, \qquad a^{-1}(t) = v^t, \qquad d = iv = 1-v",
        "derivationSteps": [
            step("현재의 1원이 한 기간 후 (1+i)가 된다는 정의(I-1)에서 출발한다. 한 기간 후 1원을 만들기 위해 지금 투자해야 할 금액을 PV라 하면, PV를 투자했을 때 한 기간 뒤 정확히 1원이 되어야 하므로:", r"PV(1+i) = 1"),
            step("이를 PV에 대해 풀면:", r"PV = \frac{1}{1+i}"),
            step("이 값을 할인인자 v로 정의한다. t시점의 1원에 대해서도 같은 논리를 반복하면:", r"v \equiv \frac{1}{1+i}, \qquad a^{-1}(t) = v^t"),
            step("한편 실할인율 d는 '1년 후 1원'과 '그것의 현재가치 v'의 차이로 정의된다:", r"d \equiv 1-v"),
            step("여기에 v=1/(1+i)를 대입하면:", r"d = 1-\frac{1}{1+i} = \frac{(1+i)-1}{1+i} = \frac{i}{1+i} = i\cdot v"),
            step("따라서 d, iv, 1−v 세 식이 모두 같은 값임이 확인된다:", r"d = iv = 1-v"),
        ],
        "derivation": "",
        "termMeanings": [term("v", "1년 후의 1원이 '오늘' 얼마의 가치를 갖는지"), term("d", "1년 후의 1원 중 '할인되어 사라지는' 부분의 비율"), term("iv", "이자율 i를 오늘 시점(할인된 금액 v) 기준으로 환산한 것")],
        "intuition": "i는 '오늘의 1원'을 기준으로 이자를 계산하는 비율(기말 기준)이고, d는 '1년 후의 1원'을 기준으로 할인폭을 계산하는 비율(기초 기준)이다. 같은 현상을 어느 시점 기준으로 재느냐만 다를 뿐이며, d=iv 관계식이 두 관점을 정확히 이어준다.",
        "relatedFormulas": "I-1의 a(t)=(1+i)ᵗ와 정확히 역수 관계. I-5의 이력 δ은 v를 극한으로 확장한 연속형 개념이다.",
        "prerequisites": ["I-1 단위종가함수"],
        "leadsTo": ["I-5 이력과 할인력", "I-6 확정연금의 현가"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 2.4·4.5 할인율", "IFRS17 11장 I-8~10 할인율 산출방법"], "IFRS17 보험부채는 미래현금흐름을 v와 같은 원리로, 다만 무위험수익률에 유동성프리미엄을 가산한 조정된 할인율로 현재가치화한 값이다."),
    },
    {
        "num": "I-4", "title": "명목이율과 명목할인율", "titleEn": "nominal rate of interest / discount", "page": 13,
        "def": "연 m회 복리계산할 때 '연간으로 환산'해 표시하는 이율 i⁽ᵐ⁾(실제 1회당 적용이율은 i⁽ᵐ⁾/m)과, 그 할인율 버전 d⁽ᵐ⁾. 수학적으로는 연간실이율 i와 등가(equivalent)가 되도록 정의된 분할복리 표시법이고, 보험수리학적으로는 월납·분기납처럼 연 1회보다 자주 발생하는 현금흐름을 다룰 때 이자율을 표준화하는 도구다.",
        "symbols": [sym("i", "연간 실이율"), sym("d", "연간 실할인율"), sym("i⁽ᵐ⁾", "연 m회 복리의 명목이율"), sym("d⁽ᵐ⁾", "연 m회 복리의 명목할인율"), sym("m", "연간 복리계산(또는 할인계산) 횟수")],
        "assumptions": ["m은 1보다 큰 양의 정수", "명목이율/명목할인율은 항상 연간실이율 i(또는 d)와 '동가(equivalent)'가 되도록 정의됨"],
        "formula": r"1+i = \left(1+\frac{i^{(m)}}{m}\right)^{m}, \qquad 1-d = \left(1-\frac{d^{(m)}}{m}\right)^{m}",
        "derivationSteps": [
            step("연간실이율 i로 1년 동안 불어난 금액과, 명목이율 i⁽ᵐ⁾으로 연 m회 복리계산해 1년 동안 불어난 금액이 서로 같아야 한다는 '동가 조건'에서 출발한다. m회 복리에서 1회(1/m년)당 실이율은 i⁽ᵐ⁾/m이므로, 1년(m번 복리) 후 종가는:", r"\left(1+\frac{i^{(m)}}{m}\right)^m"),
            step("이 값이 연간실이율 i로 계산한 1년 후 종가 (1+i)와 같아야 하므로:", r"1+i = \left(1+\frac{i^{(m)}}{m}\right)^m"),
            step("이 식을 i⁽ᵐ⁾에 대해 풀면(양변에 1/m제곱):", r"(1+i)^{1/m} = 1+\frac{i^{(m)}}{m}"),
            step("정리하면:", r"i^{(m)} = m\left[(1+i)^{1/m}-1\right]"),
            step("명목할인율 d⁽ᵐ⁾도 같은 논리를 '할인' 방향으로 적용한다. d로 1년 할인한 것과 d⁽ᵐ⁾으로 m회 나눠 할인한 것이 동가여야 하므로:", r"1-d = \left(1-\frac{d^{(m)}}{m}\right)^m \;\Longrightarrow\; d^{(m)} = m\left[1-(1-d)^{1/m}\right]"),
        ],
        "derivation": "",
        "termMeanings": [term("i⁽ᵐ⁾/m", "1회 복리계산 기간(1/m년)당 실제 적용되는 이율"), term("m", "1년을 몇 등분해 복리계산하는지를 나타내는 지수")],
        "intuition": "명목이율은 '실제로 그 기간에 적용되는 이율'이 아니라 '연간으로 환산해 부르기 편하게 만든 이름'이다. m>1이고 i>0인 경우, i⁽ᵐ⁾은 i보다 항상 작다 — 더 자주 복리계산할수록 같은 연간실이율을 만들기 위해 필요한 1회당 이율(및 그 m배인 명목이율)이 줄어들기 때문이다(오목함수 (1+i)^(1/m)의 성질에서 유도되는 결과이며, m=1이면 i⁽ᵐ⁾=i로 같아진다).",
        "relatedFormulas": "m→∞ 극한을 취하면 I-5의 이력 δ으로 수렴한다(i⁽ᵐ⁾→δ, d⁽ᵐ⁾→δ).",
        "prerequisites": ["I-1 단위종가함수", "I-3 현가와 할인"],
        "leadsTo": ["I-5 이력과 할인력", "II-1 확정연금(전화기간<지급기간)"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="복리계산 주기 환산은 순수 이자론 계산기법으로, 해설서에서 이 항등식을 별도 조문으로 다루지는 않는다. 다만 할인율을 실무적으로 적용할 때(예: 월단위 현금흐름 할인) 배경 지식으로 쓰인다."),
    },
    {
        "num": "I-5", "title": "이력과 할인력", "titleEn": "force of interest", "page": 17,
        "def": "특정 순간의 순간이율(instantaneous rate) δₜ. 수학적으로는 종가함수의 로그미분이고, 보험수리학적으로는 복리계산 빈도를 무한대로 보낸 '연속복리'의 이율이며, 이후 2장에서 정의되는 사력 μ(x)와 정확히 대칭되는 구조로 다시 등장한다.",
        "symbols": [sym("δₜ", "t시점의 이력(순간이율)"), sym("δ", "복리 하에서 t와 무관하게 일정한 이력값"), sym("a'(t)", "종가함수의 순간 증가속도(도함수)")],
        "assumptions": ["a(t)가 미분가능", "복리 가정 하에서는 δ가 t에 무관한 상수가 됨(단리에서는 δₜ가 t에 따라 변함)"],
        "formula": r"\delta_t = \frac{a'(t)}{a(t)} = \frac{d}{dt}\ln a(t), \qquad \delta = \ln(1+i) \;\text{(복리, 상수)}, \qquad a(t)=e^{\delta t}",
        "derivationSteps": [
            step("복리 a(t)=(1+i)ᵗ의 양변에 자연로그를 취하면:", r"\ln a(t) = t \ln(1+i)"),
            step("이를 t로 미분하면:", r"\frac{a'(t)}{a(t)} = \ln(1+i)"),
            step("이 값은 t에 무관한 상수이므로 이를 이력 δ로 정의한다:", r"\delta \equiv \ln(1+i)"),
            step("역으로 δ가 상수라는 정의에서, dln a(t)/dt=δ를 t에 대해 적분하면:", r"\ln a(t) = \delta t \;\Longrightarrow\; a(t) = e^{\delta t}"),
        ],
        "derivation": "",
        "termMeanings": [term("a'(t)", "종가함수의 순간 증가속도"), term("a'(t)/a(t)", "현재 잔고 대비 순간 증가속도의 비율(=순간이율)")],
        "intuition": "명목이율(I-4)이 '연 몇 회'라는 이산적 복리 빈도를 다뤘다면, 이력은 그 빈도를 무한대로 보낸 극한(연속복리)의 이율이다. 이자론에서 가장 이론적으로 깔끔한 형태이며, 확률모형(2장의 사력 μ(x))과 정확히 대칭되는 구조로 재등장한다.",
        "relatedFormulas": "2장의 사력 μ(x)=−S'(x)/S(x)와 부호만 반대인 쌍둥이 개념(a는 증가함수, S는 감소함수). I-4의 m→∞ 극한이기도 하다.",
        "prerequisites": ["I-1 단위종가함수", "I-4 명목이율과 명목할인율"],
        "leadsTo": ["I-6 확정연금의 현가", "2장 II-5 사력"],
        "ifrs17": ifrs("직접적인 수리적 기반", ["IFRS17 11장 I-8~10 할인율 산출방법(조정무위험금리기간구조)"], "IFRS17 할인율은 실무적으로 만기별 스팟금리(이산 기간구조)로 고시되지만, 그 이론적 배경은 이 연속복리 개념과 동일한 화폐의 시간가치 원리다."),
    },
    {
        "num": "I-6", "title": "확정연금 (전화기간 = 매회 지급기간)", "titleEn": "annuity-immediate", "page": 21,
        "def": "매 기말(1년마다) 1씩 정확히 n회 지급하는 유기연금(기말급, annuity-immediate)의 현재가치. 수학적으로는 등비수열의 합이고, 보험수리학적으로는 이후 생명연금(4장)에서 생존확률이 곱해진 형태로 그대로 확장되는 원형이다.",
        "symbols": [sym("a‾n|", "n년 기말급 확정연금의 현가율"), sym("n", "총 지급횟수(년)")],
        "assumptions": ["매 기말 1씩 정확히 n회 지급(기시급이 아닌 기말급)", "이자전화주기 = 지급주기 = 1년"],
        "formula": r"a_{\overline{n}|} = v + v^2 + \cdots + v^n = \frac{1-v^n}{i}",
        "derivationSteps": [
            step("각 지급시점 k=1,…,n에 지급되는 1의 현재가치는 vᵏ이므로, 전체 현가는 이 값들의 합이다:", r"a_{\overline{n}|} = v+v^2+\cdots+v^n"),
            step("이는 첫항 v, 공비 v, 항수 n인 등비수열의 합이므로 등비급수 공식을 적용하면:", r"a_{\overline{n}|} = v\cdot\frac{1-v^n}{1-v}"),
            step("I-3에서 1−v=iv였음을 이용해 분모를 치환하면:", r"a_{\overline{n}|} = \frac{v(1-v^n)}{iv} = \frac{1-v^n}{i}"),
        ],
        "derivation": "",
        "termMeanings": [term("1−vⁿ", "n년째 만기의 1원과 그 현재가치의 차이(=n년 동안 할인되어 사라진 부분)"), term("÷i", "그 차이를 이자율 i로 나눠 매년 균등하게 갚는다는 연금의 성격을 반영")],
        "intuition": "확정연금 현가는 '각 회차 지급액을 개별적으로 할인해서 더한 값'일 뿐이지만, 등비수열이라는 성질 덕분에 닫힌 형태 (1−vⁿ)/i로 압축된다. 이후 등장하는 거의 모든 연금·보험 공식이 이 등비급수 정리 기법을 반복해서 사용한다.",
        "relatedFormulas": "생명연금 äx(4장)는 여기에 생존확률 ₖpₓ를 추가로 곱한 확장형이다.",
        "prerequisites": ["I-3 현가와 할인"],
        "leadsTo": ["I-8 변동연금", "4장 생명연금"],
        "ifrs17": ifrs("강한 개념적 연관", ["IFRS17 4.4 현금흐름의 특성과 포함항목"], "여러 시점에 걸친 확정 현금흐름을 현재가치로 합산한다는 구조 자체가 이행현금흐름 계산의 원형이지만, IFRS17 현금흐름은 확률적(비확정) 급부를 다룬다는 점에서 이 항목과는 차이가 있다."),
    },
    {
        "num": "I-7", "title": "확정연금 (전화기간 > 매회 지급기간)", "page": 29,
        "def": "이자 전화(복리계산) 주기가 지급주기보다 짧은 경우(예: 월복리인데 연 1회 지급)의 연금 현가 계산법. 수학적으로는 등가이율 환산 문제이고, 보험수리학적으로는 실무에서 이자계산 주기와 보험료·급부 지급주기가 다를 때 항상 필요한 절차다.",
        "symbols": [sym("i⁽ᵐ⁾", "월(또는 더 짧은 주기) 복리의 명목이율"), sym("j", "지급주기 1회에 해당하는 등가 실이율"), sym("m", "연간 복리계산 횟수")],
        "assumptions": ["명목이율 i⁽ᵐ⁾로 m회 복리계산", "지급은 그보다 긴 주기(예: 연 1회)로 발생"],
        "formula": r"j = \left(1+\frac{i^{(m)}}{m}\right)^{(\text{지급주기}\times m)} - 1",
        "derivationSteps": [
            step("지급주기 동안 실제로 몇 번의 복리계산이 일어나는지(지급주기×m)를 구한다.", None),
            step("I-4의 등가 개념을 이용해, 그 지급주기 전체를 '1기간'으로 하는 실이율 j로 먼저 환산한다:", r"1+j = \left(1+\frac{i^{(m)}}{m}\right)^{(\text{지급주기}\times m)}"),
            step("이후로는 I-6의 표준 연금현가식 a‾n|(j)를 j를 이용해 그대로 적용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [term("j", "지급주기를 '1기간'으로 삼았을 때의 실이율")],
        "intuition": "복리 주기와 지급 주기가 다르면 공식을 새로 유도할 필요 없이, 항상 '지급주기 = 1기간'이 되도록 이자율을 먼저 환산하고 나면 표준 연금공식을 그대로 쓸 수 있다는 실무적 요령이다.",
        "relatedFormulas": "I-4의 등가이율 환산 논리를 그대로 응용.",
        "prerequisites": ["I-4 명목이율과 명목할인율", "I-6 확정연금"],
        "leadsTo": ["II-1 확정연금(전화기간<지급기간)"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="복리·지급주기 불일치 환산은 순수 계산기법으로 해설서 조문과 직접 대응되지 않는다."),
    },
    {
        "num": "I-8", "title": "기본적인 변동연금 (전화기간 = 매회 지급기간)", "titleEn": "increasing annuity", "page": 36,
        "def": "지급액이 매 기 1, 2, 3, …, n으로 매년 1씩 증가하는 누가연금(증가연금). 수학적으로는 가중등비수열의 합이고, 보험수리학적으로는 인플레이션 연동형 급부나 나이 든 계약자일수록 위험이 커지는 상품의 급부구조를 다룰 때 응용된다.",
        "symbols": [sym("(Ia)‾n|", "n년 기말급 누가연금의 현가율"), sym("ä‾n|", "n년 기시급 확정연금의 현가율")],
        "assumptions": ["k번째 지급액이 정확히 k (k=1,…,n)", "기말급"],
        "formula": r"(Ia)_{\overline{n}|} = \sum_{k=1}^{n} k v^k = \frac{\ddot a_{\overline{n}|} - n v^n}{i}",
        "derivationSteps": [
            step("Σkvᵏ (k=1..n)를 지급액 크기별로 재배열하면, '1이 n번'+'추가된 1이 n−1번'+⋯+'마지막 추가된 1이 1번' 지급되는 구조로 볼 수 있다. 이는 서로 다른 길이의 기시급 연금들의 합과 같다:", r"(Ia)_{\overline{n}|} = \ddot a_{\overline{n}|} + \ddot a_{\overline{n-1}|} + \cdots + \ddot a_{\overline{1}|}"),
            step("이 합을 정리하면(등비급수의 합의 합) 닫힌 형태가 유도된다:", r"(Ia)_{\overline{n}|} = \frac{\ddot a_{\overline{n}|} - n v^n}{i}"),
        ],
        "derivation": "",
        "termMeanings": [term("ä‾n|", "기시급 확정연금 현가율(I-6의 지급시점만 다른 변형)"), term("nvⁿ", "n년째 마지막 지급액 n의 현재가치를 보정하는 항")],
        "intuition": "매년 커지는 지급액을 하나씩 따로 계산하지 않고, '겹쳐 쌓인 여러 개의 단순연금'으로 재해석하면 복잡한 변동연금도 이미 아는 공식(I-6)의 합으로 환원된다는 대수적 요령을 보여준다.",
        "relatedFormulas": "I-6 확정연금의 직접적 확장.",
        "prerequisites": ["I-6 확정연금"],
        "leadsTo": ["II-4 연속변동연금"],
        "ifrs17": ifrs("간접적 연관", note="시간에 따라 증가하는 확정 현금흐름이라는 발상은 물가연동형 급부 설계 등에서 참고될 수 있으나, 이 항목이 해설서의 특정 조문과 직접 대응되지는 않는다."),
    },
]

II = [
    {
        "num": "II-1", "title": "확정연금 (전화기간 < 매회 지급기간)", "page": 51,
        "def": "이자 전화주기가 지급주기보다 긴 경우(예: 연복리인데 3년마다 지급)의 처리법. I-7과 반대 방향의 등가이율 환산이다.",
        "symbols": [sym("j", "지급주기(p년)에 해당하는 다기간 실이율"), sym("i", "연간 실이율"), sym("p", "지급주기(년, p>1)")],
        "assumptions": ["연간실이율 i로 매년 복리", "지급은 매 p년마다(p는 1보다 큰 정수) 발생"],
        "formula": r"j = (1+i)^p - 1",
        "derivationSteps": [
            step("p년 동안 매년 복리로 불어나는 배율은 (1+i)ᵖ이다(I-1).", r"a(p) = (1+i)^p"),
            step("이 p년 전체를 '1기간'으로 볼 때의 등가 실이율 j는, 그 기간의 종가배율에서 원금 1을 뺀 값이다:", r"j = (1+i)^p - 1"),
            step("이후 I-6의 표준 연금현가식을 j를 이용해 그대로 적용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [term("(1+i)ᵖ", "p년 동안 누적되는 복리 배율")],
        "intuition": "I-7과 정반대 방향이지만 원리는 같다 — 항상 '지급주기를 1기간으로 만드는 등가이율'을 먼저 구하고 표준공식을 적용한다.",
        "relatedFormulas": "I-7과 쌍을 이루는 반대방향 환산.",
        "prerequisites": ["I-1 단위종가함수", "I-6 확정연금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-2", "title": "연속확정연금", "titleEn": "continuous annuity", "page": 53,
        "def": "지급이 매 순간 연속적으로 이루어지는 극한적 연금. 수학적으로는 이산합이 적분으로 대체된 극한이고, 보험수리학적으로는 사망즉시급(3장)처럼 '순간에 발생하는' 급부를 다룰 때 필요한 연속형 도구다.",
        "symbols": [sym("ā‾n|", "n년 연속연금의 현가율"), sym("δ", "이력(I-5)")],
        "assumptions": ["지급이 [0,n] 구간에서 매 순간 밀도 1로(단위시간당 1씩) 발생"],
        "formula": r"\bar a_{\overline{n}|} = \frac{1-v^n}{\delta} = \int_0^n v^t \, dt",
        "derivationSteps": [
            step("I-6의 a‾n|=(1−vⁿ)/i에서 연간 지급횟수 m을 무한히 늘리는 극한을 취한다.", None),
            step("I-5에서 명목이율 i⁽ᵐ⁾이 m→∞일 때 이력 δ로 수렴함을 보였으므로, 분모의 i가 δ로 대체된다:", r"\bar a_{\overline{n}|} = \lim_{m\to\infty} a_{\overline{n}|}^{(m)} = \frac{1-v^n}{\delta}"),
            step("적분 표현은 [0,n] 구간에서 매 순간 vᵗ만큼 할인된 무한소 지급액을 전부 더한 것과 같다:", r"\bar a_{\overline{n}|} = \int_0^n v^t\,dt"),
        ],
        "derivation": "",
        "termMeanings": [term("δ", "연속복리 하에서의 순간이율(I-5)")],
        "intuition": "이산적인 연금 지급을 '무한히 잘게 쪼갠' 극한이며, 수학적으로는 적분으로 표현되지만 결과식의 형태는 이산형과 거의 같고 i만 δ로 바뀐다.",
        "relatedFormulas": "I-6의 연속형 극한.",
        "prerequisites": ["I-5 이력과 할인력", "I-6 확정연금"],
        "leadsTo": ["4장 II-3 연속생명연금"],
        "ifrs17": ifrs("간접적 연관", note="연속시간 모형은 이론적 배경으로 쓰이며, 11장에서 실제 IFRS17 계산에 쓰이는 방식은 이산(월별) 방식이다."),
    },
    {
        "num": "II-3", "title": "일반적인 변동연금", "page": 58,
        "def": "지급액이 등차·등비 등 임의의 규칙으로 변하는 연금의 일반형. I-6·I-8이 이 일반형의 특수 사례임을 보여준다.",
        "symbols": [sym("bₖ", "k시점의 지급액(임의의 수열)"), sym("PV", "연금의 현재가치")],
        "assumptions": ["각 시점의 지급액 bₖ가 미리 정해진 수열로 주어짐"],
        "formula": r"PV = \sum_{k} b_k v^k",
        "derivationSteps": [
            step("연금현가의 정의(각 시점 지급액에 그 시점 할인계수를 곱해 합산)를, 지급액이 일정하다는 가정 없이 그대로 일반화한 것이다:", r"PV = \sum_k b_k v^k"),
        ],
        "derivation": "",
        "termMeanings": [term("bₖ", "등차(I-8)/등비/임의 수열 등 어떤 규칙이든 대입 가능")],
        "intuition": "I-6(bₖ=1 상수), I-8(bₖ=k 등차)가 이 일반식의 특수 사례임을 보여주는 상위 개념이다.",
        "relatedFormulas": "I-6(bₖ=1), I-8(bₖ=k)의 일반화.",
        "prerequisites": ["I-6 확정연금", "I-8 변동연금"],
        "leadsTo": ["II-4 연속변동연금"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-4", "title": "연속변동연금", "page": 62,
        "def": "(Iā)‾n| 등 연속시간에서의 변동지급 연금. I-8(변동)과 II-2(연속)를 동시에 적용한 결과다.",
        "symbols": [sym("(Iā)‾n|", "연속 누가연금의 현가율")],
        "assumptions": ["지급률이 시간에 비례해 연속적으로 증가"],
        "formula": r"(I\bar a)_{\overline{n}|} = \frac{\ddot a_{\overline n|} - n v^n}{\delta}",
        "derivationSteps": [
            step("I-8의 이산형 변동연금식에서 지급횟수를 무한히 늘리는 극한을 취하면, 이산합 Σ가 적분으로, 실이율 i가 이력 δ로 치환된다:", r"(I\bar a)_{\overline{n}|} = \frac{\ddot a_{\overline n|} - n v^n}{\delta}"),
        ],
        "derivation": "",
        "termMeanings": [],
        "intuition": "I-8과 II-2를 동시에 적용한 결과 — 변동(증가) + 연속(순간지급)의 결합.",
        "relatedFormulas": "I-8, II-2의 결합.",
        "prerequisites": ["I-8 변동연금", "II-2 연속확정연금"],
        "leadsTo": [],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-5", "title": "기간과 이율이 미지수인 경우", "page": 64,
        "def": "연금현가식 a‾n|=K를 만족하는 미지의 n 또는 i를 역산하는 문제(예: 대출 상환기간 산정).",
        "symbols": [sym("K", "주어진 목표 현가(기지값)"), sym("n", "미지수인 지급횟수"), sym("i", "미지수일 수도 있는 이자율")],
        "assumptions": ["연금의 다른 조건(지급액, 그리고 이율 또는 기간 중 하나)은 이미 고정되어 있음"],
        "formula": r"n = \frac{\ln(1-Ki)}{\ln v}",
        "derivationSteps": [
            step("연금현가식 (1−vⁿ)/i=K를 vⁿ에 대해 정리하면:", r"v^n = 1-Ki"),
            step("양변에 로그를 취해 n에 대해 풀면:", r"n = \frac{\ln(1-Ki)}{\ln v}"),
            step("i가 미지수인 경우는 이 식과 달리 대수적으로 깔끔하게 풀리지 않아, 선형보간이나 Newton-Raphson 같은 수치해법을 사용한다.", None),
        ],
        "derivation": "",
        "termMeanings": [term("1−Ki", "vⁿ, 즉 n기간 후 할인계수의 값")],
        "intuition": "실무에서는 '월 얼마씩 몇 년을 갚아야 하는가'처럼 n을 구하는 문제가 흔히 등장하며, 이 식이 그 계산의 근거가 된다.",
        "relatedFormulas": "I-6 확정연금 현가식의 역산.",
        "prerequisites": ["I-6 확정연금"],
        "leadsTo": ["II-6 수익률의 측정"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음"),
    },
    {
        "num": "II-6", "title": "수익률(이회율)의 측정", "titleEn": "yield rate, internal rate of return", "page": 69,
        "def": "여러 시점에 걸친 현금흐름들의 내부수익률(IRR) — 순현재가치를 정확히 0으로 만드는 할인율.",
        "symbols": [sym("CFₜ", "t시점의 현금흐름(유입은 +, 유출은 −)"), sym("v", "구하고자 하는 할인인자")],
        "assumptions": ["시점별 현금흐름 CFₜ가 모두 확정적으로 주어져 있음"],
        "formula": r"\sum_t CF_t \, v^t = 0",
        "derivationSteps": [
            step("각 시점의 현금유입·유출에 할인계수 vᵗ를 곱해 전부 합산한 값(순현재가치)이 정확히 0이 되는 v를 찾는 방정식을 세운다:", r"\sum_t CF_t v^t = 0"),
            step("현금흐름의 부호가 여러 번 바뀌면 다항식 차수가 높아져 대수적으로 못 풀 수 있어, 이 경우 수치해법(선형보간, Newton-Raphson 등)이 쓰인다.", None),
        ],
        "derivation": "",
        "termMeanings": [term("Σ CFₜvᵗ = 0", "유입의 현가 합 = 유출의 현가 합, 이라는 손익분기 조건")],
        "intuition": "'투자의 진짜 수익률이 얼마인가'를 묻는 가장 일반적인 방법이며, 이후 7장(영업보험료)의 이익률 분석에서도 같은 논리가 재사용된다.",
        "relatedFormulas": "I-3 현가 개념의 역산 응용.",
        "prerequisites": ["I-3 현가와 할인"],
        "leadsTo": ["7장 II-3 미래손실의 분산"],
        "ifrs17": ifrs("직접 대응되는 보험회계해설서 항목 없음", note="IRR은 투자성과 평가지표로, IFRS17의 부채측정 논리(이행현금흐름)와는 목적이 다르다."),
    },
    {
        "num": "II-7", "title": "할부상환(원리금균등상환)과 감채기금", "titleEn": "amortization / sinking fund", "page": 75,
        "def": "대출을 갚는 두 가지 방식 — 원리금균등상환법(매기 동일액 X 상환)과 감채기금법(매기 이자만 내고 원금은 별도 기금에 Y씩 적립해 만기 일시상환). 둘 다 결국 원금 L을 갚는다는 목표는 같지만, 조건을 세우는 시점(현재가치 vs 미래가치)이 다르다.",
        "symbols": [sym("L", "대출원금"), sym("X", "원리금균등 상환액"), sym("Y", "감채기금 적립액"), sym("a‾n|", "n년 확정연금 현가율(I-6)"), sym("s‾n|", "n년 확정연금 종가율")],
        "assumptions": ["원리금균등상환: 매기 동일액 X를 n회 상환", "감채기금법: 매기 이자 L·i만 지급 + 별도로 Y씩 적립해 n년 후 원금 L 마련"],
        "formula": r"X = \frac{L}{a_{\overline{n}|}}, \qquad Y = \frac{L}{s_{\overline{n}|}}, \qquad s_{\overline{n}|} = a_{\overline{n}|}(1+i)^n",
        "derivationSteps": [
            step("원리금균등상환은 'X씩 n회 갚는 현금흐름의 현가가 대출원금 L과 같아야 한다'는 조건에서 출발한다:", r"X \cdot a_{\overline{n}|} = L"),
            step("이를 X에 대해 풀면:", r"X = \frac{L}{a_{\overline{n}|}}"),
            step("감채기금법은 'Y씩 n회 적립한 것의 n년 후 종가가 목표원금 L이 되어야 한다'는 조건에서 출발한다. 종가연금 s‾n|는 확정연금 a‾n|를 n년 후 시점 기준으로 환산(×(1+i)ⁿ)한 것이다:", r"Y \cdot s_{\overline{n}|} = L, \qquad s_{\overline{n}|} \equiv a_{\overline{n}|}(1+i)^n"),
            step("이를 Y에 대해 풀면:", r"Y = \frac{L}{s_{\overline{n}|}}"),
        ],
        "derivation": "",
        "termMeanings": [term("a‾n|", "매기 상환액의 현재가치 합이 대출원금과 같아야 한다는 조건에 쓰임"), term("s‾n|", "매기 적립액의 미래가치 합이 목표원금과 같아야 한다는 조건에 쓰임")],
        "intuition": "두 방식 모두 결국 '갚아야 할 원금 L'을 맞추는 것이지만, 원리금균등상환은 현재가치 기준으로, 감채기금법은 미래가치 기준으로 조건을 세운다는 관점의 차이가 있을 뿐이다.",
        "relatedFormulas": "s‾n| = a‾n|·(1+i)ⁿ 라는 항등식으로 두 식이 서로 연결된다.",
        "prerequisites": ["I-6 확정연금"],
        "leadsTo": ["7장 우리나라의 보험료산출제도"],
        "ifrs17": ifrs("간접적 연관", note="대출상환 구조 자체는 IFRS17과 무관하지만, 원금상환 스케줄을 다루는 사고방식은 계약자적립액(6장) 산출과 유사한 논리 구조를 가진다."),
    },
    {
        "num": "II-8", "title": "채권과 주식", "titleEn": "bonds and stocks", "page": 87,
        "def": "채권가격을 이표(coupon) 현금흐름과 만기상환금의 현가 합으로 계산하는 방법.",
        "symbols": [sym("F", "액면가"), sym("r", "표면이율(coupon rate)"), sym("C", "상환가액"), sym("P", "채권가격"), sym("i", "시장이자율(요구수익률)")],
        "assumptions": ["매기 이표 F·r을 n회 수령", "만기에 상환금 C 수령", "시장이자율(요구수익률) i로 할인"],
        "formula": r"P = F\!\cdot\! r \cdot a_{\overline{n}|} + C\, v^n",
        "derivationSteps": [
            step("채권 보유자의 현금흐름은 두 갈래다 — 매기 받는 이표 F·r을 n회(연금 구조), 그리고 만기에 한 번 받는 상환금 C(단일 현가). 두 현금흐름은 서로 독립적으로 발생하므로 현가를 각각 구해 더한다:", r"P = \underbrace{F\cdot r\cdot a_{\overline n|}}_{\text{이표의 현가(I-6)}} + \underbrace{C v^n}_{\text{상환금의 현가(I-3)}}"),
        ],
        "derivation": "",
        "termMeanings": [term("F·r·a‾n|", "이표 현금흐름의 현재가치"), term("C·vⁿ", "만기상환금의 현재가치")],
        "intuition": "채권가격 결정도 결국 '여러 시점의 확정 현금흐름을 현재가치로 합산'하는 I-6·I-3의 반복 적용일 뿐이라는 점에서, 이자론이 실제 금융상품 가격결정의 토대가 됨을 보여주는 사례다.",
        "relatedFormulas": "I-3(단일현가) + I-6(연금현가)의 결합.",
        "prerequisites": ["I-3 현가와 할인", "I-6 확정연금"],
        "leadsTo": [],
        "ifrs17": ifrs("간접적 연관", ["IFRS17 2장 제2절 금융상품총론"], "보험회사가 보유한 채권 자산의 평가원리이지만, 이는 보험부채가 아닌 자산측 회계(IFRS9, 해설서 2장 2절)의 영역이다."),
    },
]

data_ch1 = {
    "num": 1, "title": "이자론",
    "summary": "화폐의 시간가치를 다루는 보험수리학의 출발점. 복리·현가·할인력 등 여기서 정의되는 개념이 IFRS17 전체에서 '할인율(discount rate)'로 그대로 쓰인다.",
    "parts": [{"label": "I. 기초이론", "items": I}, {"label": "II. 일반이론", "items": II}]
}

path = r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\actuary.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for i, ch in enumerate(data["chapters"]):
    if ch["num"] == 1:
        data["chapters"][i] = data_ch1
        break
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("chapter 1 revised (audit fixes applied):", len(I) + len(II), "items")
