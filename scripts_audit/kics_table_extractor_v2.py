"""
K-ICS 지급여력비율 표 추출 v2.
v1 테스트에서 발견된 오탐 패턴을 걸러낸다:
  - '주요 경영지표' 표에서 ROA/ROE 행이 가용/요구자본으로 잘못 잡히는 경우
  - 이사회/위원회 회의록 표에서 안건명에 '지급여력비율'이라는 글자가 들어간 경우
  - RBC 비율 표(자회사·해외법인 등)가 K-ICS 표와 동일한 셀 패턴이라 섞이는 경우
  - 표 자체가 다른 계열사(예: DB생명보험)에 관한 것인데 타깃 회사 보고서 안에 같이 실린 경우

필터 규칙:
  1) 비율행 첫 셀이 '지급여력비율' 로 시작해야 함
  2) 가용자본행 첫 셀에 '(A)' 또는 '（A）' 마커가 있어야 함
  3) 요구자본행 첫 셀에 '(B)' 또는 '（B）' 마커가 있어야 함
  4) 표 바로 앞 소제목(굵은 글씨 <P> 문단)에 'RBC' 가 포함되면 제외
  5) 표 앞 900자 안에 타깃 회사명이 아닌 '~보험' 패턴의 다른 회사명이 나오면 경고 표시
"""
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TABLE_RE = re.compile(r"<TABLE\b.*?</TABLE>", re.S | re.I)
TR_RE = re.compile(r"<TR\b.*?</TR>", re.S | re.I)
CELL_RE = re.compile(r"<(TD|TH)\b[^>]*>(.*?)</\1>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
HEADING_RE = re.compile(r"<P[^>]*USERMARK=\"B\"[^>]*>(.*?)</P>", re.S | re.I)
INSURER_NAME_RE = re.compile(r"[가-힣]{2,6}(?:생명|화재|손해보험|해상보험)")


def cell_text(raw):
    return re.sub(r"\s+", " ", TAG_RE.sub("", raw)).strip()


def parse_row(tr_html):
    return [cell_text(m.group(2)) for m in CELL_RE.finditer(tr_html)]


def is_numeric_or_placeholder(s):
    s = s.strip()
    if s in ("-", "", "N/A"):
        return "empty"
    if re.fullmatch(r"-?[\d,]+(\.\d+)?", s):
        return "number"
    return "placeholder_text"


def find_kics_tables(xml_text, target_corp_name):
    results = []
    for tbl_match in TABLE_RE.finditer(xml_text):
        tbl_html = tbl_match.group(0)
        if "지급여력비율" not in tbl_html:
            continue
        rows = [parse_row(tr.group(0)) for tr in TR_RE.finditer(tbl_html)]
        rows = [r for r in rows if any(c.strip() for c in r)]

        ratio_idx = next((i for i, r in enumerate(rows) if r and r[0].startswith("지급여력비율")), None)
        if ratio_idx is None or ratio_idx < 2:
            continue

        avail_row = rows[ratio_idx - 2]
        reqd_row = rows[ratio_idx - 1]
        ratio_row = rows[ratio_idx]

        if not re.search(r"[\(（]\s*A\s*[\)）]", avail_row[0]):
            continue
        if not re.search(r"[\(（]\s*B\s*[\)）]", reqd_row[0]):
            continue

        header_row = rows[0] if rows[0][0] != avail_row[0] else None

        start = tbl_match.start()
        window = xml_text[max(0, start - 3000):start]
        headings = HEADING_RE.findall(window)
        nearest_heading = cell_text(headings[-1]) if headings else None
        if nearest_heading and "RBC" in nearest_heading:
            continue

        context_plain = re.sub(r"\s+", " ", TAG_RE.sub(" ", xml_text[max(0, start - 900):start])).strip()
        other_companies = sorted(set(
            m for m in INSURER_NAME_RE.findall(context_plain)
            if target_corp_name not in m and m not in target_corp_name
        ))

        cell_kinds = {
            "avail": [is_numeric_or_placeholder(c) for c in avail_row[1:]],
            "reqd": [is_numeric_or_placeholder(c) for c in reqd_row[1:]],
            "ratio": [is_numeric_or_placeholder(c) for c in ratio_row[1:]],
        }

        results.append({
            "nearest_heading": nearest_heading,
            "header": header_row,
            "available_capital_row": avail_row,
            "required_capital_row": reqd_row,
            "ratio_row": ratio_row,
            "cell_kinds": cell_kinds,
            "other_companies_mentioned_nearby": other_companies,
        })
    return results


def main(path, corp_name):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    tables = find_kics_tables(text, corp_name)
    print(f"파일: {path}  (타깃 회사: {corp_name})")
    print(f"필터 통과 후보 표: {len(tables)}개\n")
    for i, t in enumerate(tables, 1):
        flag = " ⚠ 다른 회사명 감지" if t["other_companies_mentioned_nearby"] else ""
        print(f"--- 후보 {i}{flag} ---")
        print("  소제목:          ", t["nearest_heading"])
        print("  헤더:            ", t["header"])
        print("  가용자본 행:      ", t["available_capital_row"], t["cell_kinds"]["avail"])
        print("  요구자본 행:      ", t["required_capital_row"], t["cell_kinds"]["reqd"])
        print("  비율 행:          ", t["ratio_row"], t["cell_kinds"]["ratio"])
        if t["other_companies_mentioned_nearby"]:
            print("  근처에 언급된 다른 회사명:", t["other_companies_mentioned_nearby"])
        print()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
