# -*- coding: utf-8 -*-
# K-ICS 해설서 구조화. offset 검증: pdf_index = printed_page + 5 (총칙 p.1→idx6, p.7→idx12 확인됨)
import json

OFFSET = 5
def pg(p): return p + OFFSET

def item(code, title, page, connect=None, strength=None):
    d = {"code": code, "title": title, "pageStart": pg(page)}
    if connect:
        d["theory"] = connect
        d["connect"] = connect
        d["strength"] = strength or "간접적 연관"
    return d

chapters = []

# ===== Ⅰ. 총칙 =====
chapters.append({
    "num": "Ⅰ", "title": "총칙", "general": True,
    "items": [
        item("1", "목적", 1),
        item("2", "용어의 정의", 1,
             "K-ICS 비율=가용자본/요구자본이라는 기본 틀과 위험마진(RA와 유사) 등 핵심 용어를 정의한다. 위험마진의 정의(장래 현금흐름 불확실성에 대비한 추가 적립)는 최신보험수리학 11장 I-3(책임준비금 구성항목의 RA)과 동일한 발상이다.",
             "강한 개념적 연관"),
        item("3", "지급여력비율 산출 원칙", 10),
        item("4", "건전성감독기준 재무상태표 작성방법", 10),
    ]
})

# ===== Ⅱ. 자산 및 부채 평가 =====
ii_items = []
ii_items.append(item("1", "총칙", 13))
ii_items.append(item("2-1", "일반원칙 (자산 및 기타부채 평가)", 19))
ii_items.append(item("2-2", "할인율 산출기준", 19,
    "K-ICS 할인율도 무위험금리+조정 구조를 쓴다는 점에서 최신보험수리학 1장(이자론)의 할인 개념과 11장 I-8(IFRS17 할인율 산출)이 그대로 배경 이론이 된다.",
    "직접적인 수리적 기반"))
ii_items.append(item("2-3", "자산 평가기준", 23))
ii_items.append(item("2-4", "기타부채 평가기준", 32))
ii_items.append(item("3-1", "일반원칙 (생명보험 및 장기손해보험 부채평가)", 34))
ii_items.append(item("3-2", "현행추정부채", 35,
    "'확률가중평균한 장래현금흐름의 현재가치'라는 현행추정부채의 정의가 최신보험수리학 3장 I-1(보험수리적현가 APV)의 정의와 사실상 동일하며, 11장 II-3(BEL 산출식)이 이를 실제로 계산하는 절차다.",
    "직접적인 수리적 기반"))
ii_items.append(item("3-3", "위험마진", 54,
    "IFRS17의 위험조정(RA)에 대응하는 개념으로, 최신보험수리학 11장 I-3, 7장 II-3(Var(L))·II-5(백분위 보험료)의 신뢰수준 논리와 통계적으로 동일한 발상이다.",
    "강한 개념적 연관"))
ii_items.append(item("3-4", "보험계약대출", 56))
ii_items.append(item("3-5", "재보험자산", 59))
ii_items.append(item("4-1", "일반원칙 (일반손해보험 부채평가)", 64))
ii_items.append(item("4-2", "현행추정부채", 65))
ii_items.append(item("4-3", "위험마진", 71))
ii_items.append(item("4-4", "재보험자산", 72))
ii_items.append(item("5-1", "일반원칙 (보험부채 할인율)", 74))
ii_items.append(item("5-2", "할인율 산출구조", 74,
    "최신보험수리학 1장 I-5(이력과 할인력)·11장 I-8(할인율 산출방법)이 이 절의 계리적 기초다.",
    "직접적인 수리적 기반"))
ii_items.append(item("5-3", "원화 할인율 산출", 75))
ii_items.append(item("5-4", "변동성 조정(Volatility Adjustment)", 83))
ii_items.append(item("5-5", "매칭 조정(Matching Adjustment)", 87))
ii_items.append(item("5-6", "해외통화의 할인율 산출", 88))
chapters.append({"num": "Ⅱ", "title": "자산 및 부채 평가", "general": False, "items": ii_items})

# ===== Ⅲ. 지급여력금액 산출 (가용자본) =====
chapters.append({
    "num": "Ⅲ", "title": "지급여력금액 산출 (가용자본)", "general": True,
    "items": [
        item("1", "개요", 91),
        item("2", "계층화", 93),
        item("3", "자본증권의 계층분류기준", 103),
    ]
})

# ===== Ⅳ. 지급여력기준금액 산출 (요구자본) =====
iv_items = []
iv_items.append(item("1-1", "측정기준", 106))
iv_items.append(item("1-2", "산출구조", 106,
    "요구자본은 여러 위험액을 상관계수로 결합해 산출하는데, 이는 최신보험수리학 8장(연생모형)에서 독립·종속 확률변수를 결합하는 논리, 9장(다중탈퇴모형)에서 여러 위험을 동시에 다루는 논리와 통계적으로 연결된다.",
    "간접적 연관"))
iv_items.append(item("1-3", "측정방식", 108))
iv_items.append(item("1-4", "편입자산분해", 109))
iv_items.append(item("1-5", "위험경감기법", 115))
iv_items.append(item("1-6", "비례성원칙(Principle of Proportionality)", 122))
iv_items.append(item("1-7", "적격 인프라투자 조건", 136))
iv_items.append(item("1-8", "종속회사 및 관계회사의 요구자본 산출", 140))
iv_items.append(item("2-1", "일반원칙 (생명·장기손해보험위험액)", 142,
    "생명보험위험액의 7개 하위위험(사망·장수·장해질병·장기재물기타·해지·사업비·대재해)은 최신보험수리학이 다루는 확률적 위험 요소들을 리스크 관리 관점에서 재분류한 것이다.",
    "강한 개념적 연관"))
iv_items.append(item("2-2", "사망위험액", 150,
    "사망률이 예상보다 '증가'하는 방향으로 충격을 주는 시나리오로, 최신보험수리학 2장(생존분포와 생명표)의 사망확률 qₓ, 3장(생명보험)의 Ax 계산이 이 위험액 산출의 계리적 기초다.",
    "직접적인 수리적 기반"))
iv_items.append(item("2-3", "장수위험액", 151,
    "사망률이 예상보다 '감소'(오래 생존)하는 방향의 위험으로, 4장(생명연금) äx 계산이 연금형 상품의 장수위험 평가에 직접 사용된다.",
    "직접적인 수리적 기반"))
iv_items.append(item("2-4", "장해·질병위험액", 152,
    "10장(다중상태모형)의 건강-질병-사망 전이확률 이론이 이 위험액의 계리적 배경이다.",
    "강한 개념적 연관"))
iv_items.append(item("2-5", "장기재물·기타위험액", 154))
iv_items.append(item("2-6", "해지위험액", 155,
    "최신보험수리학 9장(다중탈퇴모형)의 해지율 q⁽ʲ⁾ₓ, 11장 I-5~7(월별 다중탈퇴율 산출)이 해지위험액 산출의 직접적 기초다.",
    "직접적인 수리적 기반"))
iv_items.append(item("2-7", "사업비위험액", 158,
    "7장(영업보험료)의 사업비 이론이 배경이 된다.",
    "강한 개념적 연관"))
iv_items.append(item("2-8", "대재해위험액", 160))
iv_items.append(item("3-1", "일반원칙 (일반손해보험위험액)", 165))
iv_items.append(item("3-2", "보험가격·준비금위험액", 166))
iv_items.append(item("3-3", "대재해위험액", 190))
iv_items.append(item("4-1", "일반원칙 (시장위험액)", 199))
iv_items.append(item("4-2", "금리위험액", 200,
    "금리 충격 시나리오로 자산·부채 가치 변동을 측정하는데, 최신보험수리학 1장(이자론)·11장 I-9~10(결정론적/확률론적 할인율 시나리오)이 그대로 계리적 기초다.",
    "직접적인 수리적 기반"))
iv_items.append(item("4-3", "주식위험액", 209))
iv_items.append(item("4-4", "부동산위험액", 226))
iv_items.append(item("4-5", "외환위험액", 227))
iv_items.append(item("4-6", "자산집중위험액", 233))
iv_items.append(item("5-1", "익스포져 산출기준 (신용위험액)", 242))
iv_items.append(item("5-2", "신용위험액 산출기준", 251))
iv_items.append(item("5-3", "신용위험액 위험경감기법", 261))
iv_items.append(item("6-1", "익스포져 산출기준 (운영위험액)", 265))
iv_items.append(item("6-2", "운영위험액 산출기준", 268))
iv_items.append(item("7", "요구자본에 대한 법인세효과", 270))
chapters.append({"num": "Ⅳ", "title": "지급여력기준금액 산출 (요구자본)", "general": False, "items": iv_items})

# ===== Ⅴ. 문서화 요건 =====
chapters.append({"num": "Ⅴ", "title": "문서화 요건", "general": True, "items": [item("1", "개요", 277)]})

# ===== Ⅵ. 경과조치 =====
chapters.append({
    "num": "Ⅵ", "title": "경과조치", "general": True,
    "items": [
        item("1", "경과조치 모델", 282),
        item("2", "경과조치 적용 및 종료", 293),
    ]
})

data = {"pageCounts": {"kics": 306}, "chapters": chapters}
with open(r"C:\Users\엄제현\Desktop\ifrs17-site-web\data\kics.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

n_items = sum(len(c["items"]) for c in chapters)
n_conn = sum(1 for c in chapters for it in c["items"] if it.get("connect"))
print(f"wrote kics.json: {len(chapters)} parts, {n_items} items, {n_conn} with 보험수리학 연결")
