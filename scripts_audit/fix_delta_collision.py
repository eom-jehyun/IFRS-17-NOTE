# -*- coding: utf-8 -*-
r"""
δ 기호 혼용 해소.

문제:
  1~6장에서 δ 는 '이력(force of interest)' 이다.  a(t)=e^{δt},  δ=ln(1+i)
  11~12장에서는 같은 δ 를 '할인율' 로 쓰면서 (1+δ) 형태로 곱한다. 이는 실이율(연복리)이며
  이력과 다른 양이다.  e^δ ≠ 1+δ.
  특히 12장 I-3 은 기호를 "δ = 할인율(1장 I-5, 11장 I-8)" 로 선언해 두 개념을 등치시켰고,
  12장 I-6 은 (1+δ) 이자부리를 "6장 II-7 미분방정식의 δV(t) 항"과 같다고 서술했다.

조치:
  11~12장의 '할인율' 의미의 δ 를 r 로 바꾼다.
  근거: 『최신보험수리학』 11장 8~9절(p.1078~1079)은 이 값을 '조정무위험금리 기간구조'
  즉 기본무위험금리 + 유동성프리미엄으로 산출되는 시장 현물금리(연복리)로 설명하며,
  이력이 아니라 금리(rate)로 다룬다. 무위험수익률 기호가 이미 r_f 이므로 조정 후를 r 로
  두는 것이 자연스럽다.
  1~6장의 이력 δ 는 그대로 둔다(정당한 사용).
"""
import json
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PATH = "data/actuary.json"

# 소문자 델타만 치환한다. \Delta / Δ (변동분 표기)는 절대 건드리지 않는다.
LATEX_DELTA = re.compile(r"\\delta")
GREEK_DELTA = re.compile(r"δ")


def swap(s):
    if not isinstance(s, str):
        return s
    return GREEK_DELTA.sub("r", LATEX_DELTA.sub("r", s))


def walk(item):
    item["formula"] = swap(item.get("formula", ""))
    for st in item.get("derivationSteps") or []:
        if "text" in st:
            st["text"] = swap(st["text"])
        if "eq" in st:
            st["eq"] = swap(st["eq"])
    for s in item.get("symbols") or []:
        s["sym"] = swap(s.get("sym", ""))
        s["meaning"] = swap(s.get("meaning", ""))
    for t in item.get("termMeanings") or []:
        t["term"] = swap(t.get("term", ""))
        t["meaning"] = swap(t.get("meaning", ""))
    for k in ("def", "intuition", "relatedFormulas", "derivation"):
        if k in item:
            item[k] = swap(item[k])


# 치환 후 덮어쓸 정밀 수정 (기호 정의·경계 서술)
OVERRIDE = {}

OVERRIDE[(11, "I-8")] = {
    "symbols": [
        {"sym": "r_f(t)", "meaning": "만기 t의 기본무위험금리(현물금리)"},
        {"sym": "LP", "meaning": "유동성프리미엄(liquidity premium). 감독규정상 기간에 관계없이 단일값을 적용"},
        {"sym": "r(t)", "meaning": "만기 t의 조정무위험금리(= 기본무위험금리 + 유동성프리미엄). 연복리 기준 실이율이며, 1장 I-5의 이력 δ와는 다른 양이다"},
        {"sym": "t", "meaning": "만기(년). 할인율이 만기별로 다른 기간구조를 가진다"},
    ],
    "termMeanings": [
        {"term": "r_f(t)", "meaning": "시장에서 관찰되는 무위험 수익률. 화폐의 시간가치 자체를 담는 항"},
        {"term": "LP", "meaning": "보험부채가 시장성 자산보다 유동성이 낮다는 특성을 반영해 가산하는 부분. 이 값이 커지면 할인율이 올라가 부채 현재가치가 작아진다"},
        {"term": "r(t)", "meaning": "실제 BEL 할인에 쓰이는 최종 금리. 만기마다 값이 다르므로 하나의 숫자가 아니라 곡선(기간구조)이다"},
    ],
    "relatedFormulas": (
        "1장 I-3의 현가·할인 개념을 만기별 기간구조로 확장한 것이다. "
        "주의: 1장 I-5의 이력 δ와 여기의 r(t)는 서로 다른 양이며 δ = ln(1+r), r = e^δ − 1 의 관계로 환산된다. "
        "이 책 11장 I-9(결정론적 시나리오)와 I-10(확률론적 시나리오)에서 이 r(t)를 실제 할인에 사용한다."
    ),
}

OVERRIDE[(11, "I-9")] = {
    "symbols": [
        {"sym": "BEL", "meaning": "최선추정부채(현금흐름의 기대현재가치)"},
        {"sym": "CF_t", "meaning": "t시점의 순현금흐름(유출−유입)"},
        {"sym": "r(s)", "meaning": "만기 s의 조정무위험금리(I-8). 연복리 실이율이므로 (1+r)로 할인한다"},
        {"sym": "t, s", "meaning": "경과기간(시점). s ≤ t 구간의 금리를 누적해 t시점 현금흐름을 할인한다"},
    ],
}

OVERRIDE[(12, "I-3")] = {
    "symbols": [
        {"sym": "r", "meaning": "보험부채에 적용하는 할인율(11장 I-8의 조정무위험금리). 연복리 실이율이며 1장 I-5의 이력 δ와 다른 양이다"},
        {"sym": "BEL", "meaning": "최선추정부채"},
        {"sym": "GMA / VFA", "meaning": "일반모형 / 변동수수료모형"},
    ],
}

OVERRIDE[(12, "I-6")] = {
    "symbols": [
        {"sym": "BEL₀, BEL₁", "meaning": "기시·기말 최선추정부채"},
        {"sym": "r", "meaning": "기시에 적용한 할인율(11장 I-8). 연복리 실이율이므로 이자부리는 (1+r)를 곱한다"},
        {"sym": "Δ비금융", "meaning": "사망률·해지율 등 비금융 가정변동에 따른 BEL 변동분"},
        {"sym": "Δ금융", "meaning": "할인율 등 금융 가정변동에 따른 BEL 변동분"},
        {"sym": "CF실제", "meaning": "당기 중 실제로 발생한 현금흐름"},
    ],
    "termMeanings": [
        {
            "term": "BEL₀(1+r)",
            "meaning": "①이자부리. 기시 부채에 1년치 이자가 붙어 부채가 커지는 부분이다. "
                       "6장 II-7 Thiele 미분방정식의 δV(t) 항과 '적립액이 이자로 불어난다'는 발상은 같지만, "
                       "그쪽은 연속모형의 이력 δ이고 여기는 연 단위 실이율 r이라 기호와 계산방식이 다르다.",
        },
        {"term": "Δ비금융", "meaning": "②비금융가정변동. 실제 사망·해지 실적이 가정과 달랐을 때 발생하는 차이"},
        {"term": "Δ금융", "meaning": "③금융가정변동. 결산시점 할인율이 이전과 달라졌을 때의 재평가 효과"},
        {"term": "−CF실제", "meaning": "④당기현금흐름. 당기에 실제로 지급·수취가 일어나 부채에서 빠져나간 부분"},
    ],
}

OVERRIDE[(12, "I-7")] = {
    "symbols": [
        {"sym": "RA₀, RA₁", "meaning": "기시·기말 위험조정"},
        {"sym": "r", "meaning": "할인율(11장 I-8). 연복리 실이율"},
    ],
}

OVERRIDE[(12, "I-8")] = {
    "symbols": [
        {"sym": "CSM₀, CSM₁", "meaning": "기시·기말 보험계약마진"},
        {"sym": "r", "meaning": "CSM에 부리하는 할인율. 일반모형(GMA)에서는 최초인식시점에 확정된 할인율을 계속 사용한다"},
    ],
}


def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)

    changed = []
    for ch in data["chapters"]:
        if ch["num"] not in (11, 12):
            continue  # 1~6장의 이력 δ 는 정당한 사용이므로 건드리지 않는다
        for part in ch["parts"]:
            for item in part["items"]:
                before = json.dumps(item, ensure_ascii=False)
                walk(item)
                key = (ch["num"], item["num"])
                if key in OVERRIDE:
                    item.update(OVERRIDE[key])
                if json.dumps(item, ensure_ascii=False) != before:
                    changed.append(f"Ch{ch['num']} {item['num']} {item['title']}")

    # 1장 I-5(이력 정의)에 두 기호의 관계를 명시해 혼동을 예방한다.
    for ch in data["chapters"]:
        if ch["num"] != 1:
            continue
        for part in ch["parts"]:
            for item in part["items"]:
                if item["num"] == "I-5":
                    item["relatedFormulas"] = (
                        "I-1의 a(t)를 미분해 얻는 순간증가율이며, I-3의 v·d와 함께 이자론의 기본 4개 지표를 이룬다. "
                        "주의: 11~12장에서 IFRS17 보험부채 할인에 쓰는 r(조정무위험금리)은 연복리 실이율이라 "
                        "여기의 이력 δ와 다른 양이다. 두 값은 δ = ln(1+r), r = e^δ − 1 로 환산된다."
                    )
                    changed.append(f"Ch1 {item['num']} {item['title']} (교차참조 주석 추가)")

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"수정된 항목 {len(changed)}개")
    for c in changed:
        print("  ✔", c)


if __name__ == "__main__":
    main()
