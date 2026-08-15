# -*- coding: utf-8 -*-
r"""
LaTeX 명령어 토큰 검사.

기호 치환을 하다 보면 "\times\delta" 가 "\timesr" 처럼 붙어버려
존재하지 않는 명령이 만들어질 수 있다(실제로 발생함).
중괄호 균형 검사로는 잡히지 않으므로 KaTeX가 아는 명령어 목록과 대조한다.
"""
import json
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 이 프로젝트의 수식에서 실제로 쓰는 LaTeX 명령어
ALLOWED = {
    "frac", "tfrac", "dfrac", "binom", "sum", "prod", "int", "sqrt",
    "left", "right", "big", "Big", "bigg", "Bigg",
    "dots", "vdots", "ddots", "dotsb", "dotsc",
    "quad", "qquad", "text", "mathrm", "bar", "ddot", "dot", "hat", "tilde", "overline",
    "underbrace", "overbrace", "cdot", "cdots", "ldots", "times", "div", "pm", "mp",
    "le", "ge", "ne", "approx", "equiv", "sim", "propto", "infty", "partial",
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta", "theta",
    "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma", "tau", "upsilon",
    "phi", "varphi", "chi", "psi", "omega",
    "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Upsilon", "Phi", "Psi", "Omega",
    "to", "rightarrow", "leftarrow", "Rightarrow", "Leftarrow", "longrightarrow",
    "xrightarrow", "iff", "implies", "Longrightarrow",
    "begin", "end", "cases", "array", "matrix", "pmatrix", "bmatrix",
    "lim", "ln", "log", "exp", "max", "min", "sup", "inf", "det", "Pr",
    "phantom", "hspace", "vspace", "space", ",", ";", ":", "!",
    "mathbb", "mathcal", "mathbf", "mathit", "operatorname", "colon",
    "lvert", "rvert", "lVert", "rVert", "vert", "Vert", "mid", "nmid",
    "in", "notin", "subset", "supset", "cup", "cap", "emptyset", "forall", "exists",
}

CMD = re.compile(r"\\([a-zA-Z]+)")

with open("data/actuary.json", encoding="utf-8") as f:
    data = json.load(f)

bad = []
for ch in data["chapters"]:
    for part in ch["parts"]:
        for item in part["items"]:
            targets = [("formula", item.get("formula", ""))]
            for i, st in enumerate(item.get("derivationSteps") or []):
                targets.append((f"eq{i}", st.get("eq", "")))
            for label, txt in targets:
                if not txt:
                    continue
                for m in CMD.finditer(txt):
                    name = m.group(1)
                    if name not in ALLOWED:
                        ctx = txt[max(0, m.start() - 35): m.start() + 35]
                        bad.append((ch["num"], item["num"], label, "\\" + name, ctx))

if bad:
    print(f"알 수 없는 LaTeX 명령 {len(bad)}건 — KaTeX 렌더 실패 가능\n")
    for cn, num, label, tok, ctx in bad:
        print(f"  Ch{cn} {num} [{label}]  토큰: {tok}")
        print(f"     …{ctx}…\n")
else:
    print("모든 LaTeX 명령어가 알려진 목록에 있음 (렌더 안전)")

sys.exit(1 if bad else 0)
