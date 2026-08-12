"""
K-ICS 지급여력비율(A/B) 표 추출 프로토타입.
DART 사업보고서 원문 XML(document.xml API로 받은 파일)에서
'지급여력비율' 관련 표를 찾아 가용자본/요구자본/비율 3개년 수치를 뽑는다.

전략:
1. 전체 파일을 <TABLE>...</TABLE> 블록 단위로 쪼갠다.
2. 각 표 안에서 '지급여력비율' 이라는 글자가 들어간 <TD>/<TH>가 있는 행(TR)을 찾는다.
3. 그 행을 비율(ratio) 행으로 보고, 바로 위 2개의 형제 TR을 가용자본/요구자본 행으로 간주한다.
4. 표 상단 THEAD(있으면)에서 연도 라벨을 뽑는다.
5. 숫자가 아닌 셀(예: '공시 예정')은 그대로 문자열로 남겨서 구분한다.
"""
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TABLE_RE = re.compile(r"<TABLE\b.*?</TABLE>", re.S | re.I)
TR_RE = re.compile(r"<TR\b.*?</TR>", re.S | re.I)
CELL_RE = re.compile(r"<(TD|TH)\b[^>]*>(.*?)</\1>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")


def cell_text(raw):
    return TAG_RE.sub("", raw).strip()


def parse_row(tr_html):
    return [cell_text(m.group(2)) for m in CELL_RE.finditer(tr_html)]


def find_kics_tables(xml_text):
    results = []
    for tbl_match in TABLE_RE.finditer(xml_text):
        tbl_html = tbl_match.group(0)
        if "지급여력비율" not in tbl_html:
            continue
        rows = [parse_row(tr.group(0)) for tr in TR_RE.finditer(tbl_html)]
        rows = [r for r in rows if any(c.strip() for c in r)]

        ratio_idx = None
        for i, row in enumerate(rows):
            if row and ("지급여력비율" in row[0]):
                ratio_idx = i
                break
        if ratio_idx is None:
            continue

        header_row = rows[0] if rows and rows[0] is not rows[ratio_idx] else None
        avail_row = rows[ratio_idx - 2] if ratio_idx - 2 >= 0 else None
        reqd_row = rows[ratio_idx - 1] if ratio_idx - 1 >= 0 else None
        ratio_row = rows[ratio_idx]

        # 표 시작 위치 주변 200자에서 문맥(연결/당사/별도 등) 힌트를 뽑는다
        start = tbl_match.start()
        context = xml_text[max(0, start - 400):start]
        context = TAG_RE.sub(" ", context)
        context = re.sub(r"\s+", " ", context).strip()[-200:]

        results.append({
            "header": header_row,
            "available_capital_row": avail_row,
            "required_capital_row": reqd_row,
            "ratio_row": ratio_row,
            "context_before": context,
        })
    return results


def main(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    tables = find_kics_tables(text)
    print(f"파일: {path}")
    print(f"발견된 K-ICS 후보 표: {len(tables)}개\n")
    for i, t in enumerate(tables, 1):
        print(f"--- 후보 {i} ---")
        print("  문맥(표 앞 200자):", t["context_before"])
        print("  헤더:            ", t["header"])
        print("  가용자본 행:      ", t["available_capital_row"])
        print("  요구자본 행:      ", t["required_capital_row"])
        print("  비율 행:          ", t["ratio_row"])
        print()


if __name__ == "__main__":
    main(sys.argv[1])
