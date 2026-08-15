# -*- coding: utf-8 -*-
"""최신보험수리학 모드를 이론설명 / 공식정리 / 예제 3개 서브탭으로 재구성한다."""
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

NEW = r'''let ACT_TAB = "theory";
let ACT_CTX = null;

function openActItem(ch, part, item) {
  ACT_CTX = { ch, part, item };
  ACT_TAB = "theory";
  document.getElementById("welcome").hidden = true;
  document.getElementById("viewer").hidden = false;
  document.getElementById("tabBar").hidden = true;
  document.getElementById("viewerTitle").textContent = `제${ch.num}장 ${ch.title} / ${part.label} — ${item.num} ${item.title}`;
  renderActItem();
}

function renderActItem() {
  const { ch, part, item } = ACT_CTX;
  const body = document.getElementById("viewerBody");

  if (!item.symbols) {
    body.innerHTML = `<div class="theory-panel"><div class="theory-block">
      <span class="item-code">${item.num}</span><h3>${item.title}</h3>
      <div class="theory-text">${item.def || ""}</div></div></div>`;
    renderMath(body);
    return;
  }

  const tabs = [
    ["theory", "이론설명"],
    ["formula", "공식정리"],
    ["example", item.examples ? `예제 (${item.examples.length})` : "예제"],
  ];
  const tabBar = `<div class="act-tabs">${tabs
    .map((t) => `<button class="act-tab ${ACT_TAB === t[0] ? "active" : ""}" data-acttab="${t[0]}">${t[1]}</button>`)
    .join("")}</div>`;

  let pane = "";
  if (ACT_TAB === "theory") pane = renderActTheory(item);
  else if (ACT_TAB === "formula") pane = renderActFormula(item);
  else pane = renderExamples(item, true);

  body.innerHTML = `<div class="theory-panel"><div class="theory-block">
      <span class="item-code">${item.num}</span>
      <h3>${item.title}${item.titleEn ? ` <span class="title-en">(${item.titleEn})</span>` : ""}</h3>
      ${tabBar}
      <div class="act-pane">${pane}</div>
      <p class="page-ref">출처 — 『최신보험수리학』 제${ch.num}장 ${ch.title} ${part.label}, p.${item.page} 내용을 참고하여 필자가 재구성 (원문 문장 인용 아님)</p>
    </div></div>`;

  body.querySelectorAll("[data-acttab]").forEach((b) =>
    b.addEventListener("click", () => {
      ACT_TAB = b.dataset.acttab;
      renderActItem();
    })
  );
  body.querySelectorAll("[data-actkey]").forEach((b) =>
    b.addEventListener("click", () => jumpToAct(b.dataset.actkey))
  );
  renderMath(body);
}

// 현금흐름 표 — 시점별 지급액·할인계수·현재가치를 나란히 놓아 공식 도출을 눈으로 따라가게 한다.
function renderCfTable(cf) {
  if (!cf) return "";
  const head = cf.headers.map((h) => `<th>${h}</th>`).join("");
  const rows = cf.rows
    .map(
      (r) =>
        `<tr><td class="cf-label">${r.label}</td>` +
        r.cells.map((c) => `<td>${c ? "\\(" + c + "\\)" : "—"}</td>`).join("") +
        `</tr>`
    )
    .join("");
  return `<div class="cf-wrap">
    ${cf.caption ? `<div class="cf-caption">${cf.caption}</div>` : ""}
    <div class="table-scroll"><table class="cf-table"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div>
    ${cf.note ? `<div class="cf-note">${cf.note}</div>` : ""}
  </div>`;
}

function renderActTheory(item) {
  const symbolsHtml = item.symbols.map((s) => `<li><span class="sym">${s.sym}</span> — ${s.meaning}</li>`).join("");
  const assumptionsHtml = (item.assumptions || []).map((a) => `<li>${a}</li>`).join("");
  const termsHtml = (item.termMeanings || []).map((t) => `<li><span class="sym">${t.term}</span> — ${t.meaning}</li>`).join("");
  const prereqHtml = (item.prerequisites || []).map((p) => `<span class="chip">${p}</span>`).join("");
  const leadsHtml = (item.leadsTo || []).map((p) => `<span class="chip">${p}</span>`).join("");
  const ifrs = item.ifrs17 || { strength: "직접 대응 없음" };
  const strengthClass = STRENGTH_CLASS[ifrs.strength] || "s-none";

  const narrative = (item.narrative || [])
    .map(
      (n) => `<div class="nar-block">
        ${n.heading ? `<h4 class="nar-h">${n.heading}</h4>` : ""}
        ${n.text ? `<div class="theory-text">${n.text}</div>` : ""}
        ${n.cfTable ? renderCfTable(n.cfTable) : ""}
        ${n.eq ? `<div class="nar-eq">$$${escapeLatex(n.eq)}$$</div>` : ""}
        ${n.after ? `<div class="theory-text">${n.after}</div>` : ""}
      </div>`
    )
    .join("");

  const glossary = (item.glossary || [])
    .map((g) => `<div class="gloss"><span class="gloss-t">${g.term}</span><span class="gloss-d">${g.def}</span></div>`)
    .join("");

  return `
    <div class="field"><span class="label">① 정의</span><div class="theory-text">${item.def}</div></div>
    ${symbolsHtml ? `<div class="field"><span class="label">② 기호</span><ul class="symbol-list">${symbolsHtml}</ul></div>` : ""}
    ${assumptionsHtml ? `<div class="field"><span class="label">③ 전제(가정)</span><ul class="plain-list">${assumptionsHtml}</ul></div>` : ""}
    ${narrative ? `<div class="field"><span class="label">④ 이론 전개</span>${narrative}</div>` : ""}
    <div class="field"><span class="label">⑤ 수식의 도출</span>${renderDerivation(item)}</div>
    ${termsHtml ? `<div class="field"><span class="label">⑥ 각 항의 의미</span><ul class="symbol-list">${termsHtml}</ul></div>` : ""}
    ${item.intuition ? `<div class="field"><span class="label">⑦ 직관</span><div class="theory-text">${item.intuition}</div></div>` : ""}
    ${glossary ? `<div class="field"><span class="label">⑧ 용어 정리</span><div class="gloss-wrap">${glossary}</div></div>` : ""}
    ${prereqHtml ? `<div class="field"><span class="label">⑨ 선수개념</span><div class="chips">${prereqHtml}</div></div>` : ""}
    ${leadsHtml ? `<div class="field"><span class="label">⑩ 다음 개념</span><div class="chips">${leadsHtml}</div></div>` : ""}
    <div class="field ifrs-field">
      <span class="label">⑪ IFRS17 연결</span>
      <div class="strength-row">
        <span class="ifrs-strength ${strengthClass}">${ifrs.strength}</span>
        ${ifrs.nature ? `<span class="ifrs-nature ${NATURE_CLASS[ifrs.nature] || ""}">${ifrs.nature}</span>` : ""}
      </div>
      ${ifrs.items && ifrs.items.length ? `<ul class="plain-list">${ifrs.items.map((i) => `<li>${i}</li>`).join("")}</ul>` : ""}
      ${ifrs.note ? `<div class="ifrs-note">${ifrs.note}</div>` : ""}
      ${ifrs.boundary ? `<div class="ifrs-boundary"><span class="boundary-label">연결의 한계 — 어디까지 같고 어디부터 다른가</span>${ifrs.boundary}</div>` : ""}
    </div>`;
}

function renderActFormula(item) {
  const list = (item.formulaSummary || [])
    .map(
      (f) => `<div class="fs-row">
        <div class="fs-name">${f.name}</div>
        <div class="fs-eq">$$${escapeLatex(f.eq)}$$</div>
        ${f.note ? `<div class="fs-note">${f.note}</div>` : ""}
      </div>`
    )
    .join("");
  return `
    <div class="field"><span class="label">핵심 공식</span><div class="formula-text">$$${escapeLatex(item.formula)}$$</div></div>
    ${
      list
        ? `<div class="field"><span class="label">이 절에서 정리된 공식</span><div class="fs-wrap">${list}</div></div>`
        : `<p class="na">이 절의 공식 목록은 아직 정리 중입니다. 위 핵심 공식과 [이론설명] 탭의 도출과정을 참고하세요.</p>`
    }
    ${item.relatedFormulas ? `<div class="field"><span class="label">관련 공식</span><div class="theory-text">${item.relatedFormulas}</div></div>` : ""}`;
}

'''


def main():
    with open("app.js", encoding="utf-8") as f:
        src = f.read()

    # openActItem 은 renderDerivation(350) 보다 뒤(410)에 있으므로,
    # 종료 경계는 openActItem 다음 함수인 renderMath 를 start 이후에서 찾는다.
    start = src.index("function openActItem(ch, part, item) {")
    end = src.index("function renderMath(el)", start)
    assert end > start, "함수 경계 탐색 실패"
    src = src[:start] + NEW + src[end:]

    # renderExamples 를 탭 단독 표시에서도 쓸 수 있게 확장
    old_head = 'function renderExamples(item) {\n  const ex = item.examples;\n  if (!ex || !ex.length) return "";'
    new_head = (
        "function renderExamples(item, standalone) {\n"
        "  const ex = item.examples;\n"
        '  if (!ex || !ex.length) return standalone ? \'<p class="na">이 절의 예제는 아직 준비 중입니다.</p>\' : "";'
    )
    assert old_head in src, "renderExamples 헤더를 찾지 못했습니다"
    src = src.replace(old_head, new_head)

    old_ret = '  return `<div class="field examples-field"><span class="label">⑫ 예제</span>${blocks}</div>`;'
    new_ret = '  return standalone ? blocks : `<div class="field examples-field"><span class="label">⑫ 예제</span>${blocks}</div>`;'
    assert old_ret in src, "renderExamples 반환문을 찾지 못했습니다"
    src = src.replace(old_ret, new_ret)

    with open("app.js", "w", encoding="utf-8") as f:
        f.write(src)
    print("app.js 3-탭 구조로 재구성 완료")


if __name__ == "__main__":
    main()
