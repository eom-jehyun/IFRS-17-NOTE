"""전 항목의 핵심수식 + 선언된 기호를 압축 출력해 수식 오류를 눈으로 검수한다."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/actuary.json", encoding="utf-8") as f:
    d = json.load(f)

lo = int(sys.argv[1]) if len(sys.argv) > 1 else 1
hi = int(sys.argv[2]) if len(sys.argv) > 2 else 12

for ch in d["chapters"]:
    if not (lo <= ch["num"] <= hi):
        continue
    print(f"\n{'='*78}\n[Ch{ch['num']}] {ch['title']}\n{'='*78}")
    for part in ch.get("parts", []):
        print(f"\n  ## {part.get('label')}")
        for it in part.get("items", []):
            syms = ", ".join(s.get("sym", "") for s in (it.get("symbols") or []))
            print(f"\n  {it.get('num')} {it.get('title')}  (p.{it.get('page')})")
            print(f"    F: {it.get('formula')}")
            print(f"    S: [{syms}]" if syms else "    S: *** 기호 없음 ***")
            asm = it.get("assumptions") or []
            if asm:
                for a in asm:
                    print(f"    A: {a}")
            else:
                print("    A: *** 전제 없음 ***")
            tm = it.get("termMeanings") or []
            print(f"    T: {len(tm)}개" if tm else "    T: *** 각항의미 없음 ***")
            ifrs = it.get("ifrs17") or {}
            print(f"    I: {ifrs.get('strength')} -> {ifrs.get('items')}")
