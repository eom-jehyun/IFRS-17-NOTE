let IFRS = null;
let ACT = null;
let KICS = null;
let MODE = "ifrs17"; // "ifrs17" | "actuary" | "kics"
let currentPage = 0;

async function init() {
  const [ifrsRes, actRes, kicsRes] = await Promise.all([fetch("data/toc.json"), fetch("data/actuary.json"), fetch("data/kics.json")]);
  IFRS = await ifrsRes.json();
  ACT = await actRes.json();
  KICS = await kicsRes.json();

  const total = ACT.chapters.reduce((s, c) => s + c.parts.reduce((s2, p) => s2 + p.items.length, 0), 0);
  const done = ACT.chapters.reduce((s, c) => s + c.parts.reduce((s2, p) => s2 + p.items.filter((it) => it.def).length, 0), 0);
  document.getElementById("progressNote").textContent = `현재 ${total}개 항목 중 ${done}개 작성 완료 (계속 진행 중)`;

  renderTOC();
  document.getElementById("search").addEventListener("input", onSearch);
  document.getElementById("backBtn").addEventListener("click", showWelcome);
  document.querySelectorAll(".mode-btn").forEach((btn) => {
    btn.addEventListener("click", () => switchMode(btn.dataset.mode));
  });
}

function switchMode(mode) {
  MODE = mode;
  document.querySelectorAll(".mode-btn").forEach((b) => b.classList.toggle("active", b.dataset.mode === mode));
  document.getElementById("search").value = "";

  document.getElementById("welcomeIfrs17").hidden = true;
  document.getElementById("welcomeActuary").hidden = true;
  document.getElementById("welcomeKics").hidden = true;
  document.getElementById("welcomeCompany").hidden = true;

  if (mode === "company") {
    document.getElementById("sidebarTitle").textContent = "보험사 분석";
    document.getElementById("sidebarSubtitle").textContent = "실제 공시 → IFRS17 · K-ICS → 수리적 원리";
    document.getElementById("welcomeTitle").textContent = "왼쪽에서 보험회사를 선택하세요.";
    document.getElementById("welcomeCompany").hidden = false;
    document.getElementById("tabBar").hidden = true;
    document.getElementById("search").placeholder = "보험회사명 검색 (예: 삼성생명, DB손해보험)";
    showWelcome();
    renderTOC();
    return;
  }
  document.getElementById("search").placeholder = "검색 (예: 위험조정, 할인율, CSM)";

  if (mode === "ifrs17") {
    document.getElementById("sidebarTitle").textContent = "IFRS17 보험회계해설서";
    document.getElementById("sidebarSubtitle").textContent = "↔ 최신보험수리학 이론 연계";
    document.getElementById("welcomeTitle").textContent = "왼쪽 목차에서 IFRS17 보험회계해설서의 장·절을 선택하세요.";
    document.getElementById("welcomeIfrs17").hidden = false;
    document.getElementById("tabBar").hidden = false;
  } else if (mode === "actuary") {
    document.getElementById("sidebarTitle").textContent = "최신보험수리학";
    document.getElementById("sidebarSubtitle").textContent = "↔ IFRS17 보험회계해설서 연계";
    document.getElementById("welcomeTitle").textContent = "왼쪽 목차에서 최신보험수리학의 장·절을 선택하세요.";
    document.getElementById("welcomeActuary").hidden = false;
    document.getElementById("tabBar").hidden = true;
  } else {
    document.getElementById("sidebarTitle").textContent = "K-ICS 해설서";
    document.getElementById("sidebarSubtitle").textContent = "↔ 최신보험수리학 이론 연계";
    document.getElementById("welcomeTitle").textContent = "왼쪽 목차에서 K-ICS 해설서의 장·절을 선택하세요.";
    document.getElementById("welcomeKics").hidden = false;
    document.getElementById("tabBar").hidden = false;
  }
  showWelcome();
  renderTOC();
}

function renderTOC() {
  const nav = document.getElementById("toc");
  nav.innerHTML = "";
  if (MODE === "ifrs17") renderIfrsTOC(nav);
  else if (MODE === "actuary") renderActTOC(nav);
  else if (MODE === "company") renderCompanyTOC(nav);
  else renderKicsTOC(nav);
}

function renderKicsTOC(nav) {
  for (const ch of KICS.chapters) {
    const chapterEl = document.createElement("div");
    chapterEl.className = "chapter";
    const chTitleEl = document.createElement("div");
    chTitleEl.className = "chapter-title";
    chTitleEl.textContent = `${ch.num}. ${ch.title}`;
    const itemsWrap = document.createElement("div");
    itemsWrap.className = "sections";

    for (const it of ch.items) {
      const itemEl = document.createElement("div");
      itemEl.className = "item";
      itemEl.innerHTML = `<span class="dot ${it.connect ? "theory" : "general"}"></span><span>${it.code}. ${it.title}</span>`;
      itemEl.addEventListener("click", (e) => {
        e.stopPropagation();
        openKicsItem(ch, it);
        document.querySelectorAll(".item").forEach((n) => n.classList.remove("active"));
        itemEl.classList.add("active");
      });
      itemsWrap.appendChild(itemEl);
    }
    chTitleEl.addEventListener("click", () => itemsWrap.classList.toggle("open"));
    chapterEl.appendChild(chTitleEl);
    chapterEl.appendChild(itemsWrap);
    nav.appendChild(chapterEl);
  }
}

function kicsImgSrc(pageIndex) {
  return `images/kics/${String(pageIndex).padStart(4, "0")}.jpg`;
}

function renderKicsSourcePane() {
  const total = KICS.pageCounts.kics;
  currentPage = Math.max(0, Math.min(total - 1, currentPage));
  const wrap = document.getElementById("sourcePane");
  wrap.innerHTML = `
    <div class="pane-header">
      <span>K-ICS 해설서 원문</span>
      <div class="page-nav">
        <button id="prevBtn">◀ 이전</button>
        <span>${currentPage + 1} / ${total}</span>
        <button id="nextBtn">다음 ▶</button>
      </div>
    </div>
    <div class="page-img-wrap"><img src="${kicsImgSrc(currentPage)}"></div>
  `;
  document.getElementById("prevBtn").addEventListener("click", () => { currentPage -= 1; renderKicsSourcePane(); });
  document.getElementById("nextBtn").addEventListener("click", () => { currentPage += 1; renderKicsSourcePane(); });
}

function openKicsItem(ch, it) {
  document.getElementById("welcome").hidden = true;
  document.getElementById("viewer").hidden = false;
  document.getElementById("tabBar").hidden = false;
  document.getElementById("viewerTitle").textContent = `${ch.num}. ${ch.title} — ${it.code}. ${it.title}`;
  currentPage = it.pageStart;

  const body = document.getElementById("viewerBody");
  const explainHtml = renderKicsExplain(it);
  const connectHtml = it.connect
    ? `<div class="connect-box"><span class="label">최신보험수리학과의 연결</span>${it.connect}</div>`
    : "";
  const theoryHtml =
    explainHtml || connectHtml
      ? `<div class="theory-panel"><div class="theory-block">${explainHtml}${connectHtml}</div></div>`
      : `<div class="theory-panel"><div class="general-note">이 절은 최신보험수리학과 직접 대응되는 이론이 없는 일반 금융·회계 영역입니다.</div></div>`;

  body.innerHTML = `
    <div class="tab-pane active" id="pane-source"><div class="source-viewer" id="sourcePane"></div></div>
    <div class="tab-pane" id="pane-theory">${theoryHtml}</div>
  `;
  renderKicsSourcePane();
  document.querySelectorAll(".tab-btn").forEach((btn) => btn.classList.toggle("active", btn.dataset.tab === "source"));
  wireTabs();
  // 새로 추가된 K-ICS 산출식(LaTeX)을 렌더하고, 보험수리학 이동 chip을 연결한다.
  renderMath(body);
  body.querySelectorAll("[data-actkey]").forEach((b) =>
    b.addEventListener("click", () => jumpToAct(b.dataset.actkey))
  );
}

// K-ICS 산출구조 해설 렌더링. 내용은 모두 K-ICS 해설서 원문에서 확인된 것이며 근거 페이지를 함께 표시한다.
function renderKicsExplain(it) {
  const ex = it.explain;
  if (!ex) return "";
  const qa = (ex.questions || [])
    .map((x) => `<div class="qa"><div class="qa-q">${x.q}</div><div class="qa-a">${x.a}</div></div>`)
    .join("");
  const lineage = (ex.lineage || []).map((l) => `<span class="chip">${l}</span>`).join("");
  const al = ex.actuarialLink;
  const alHtml = al
    ? `<div class="field">
         <span class="label">보험수리학과의 연결</span>
         <div class="theory-text">${al.note}</div>
         <div class="chips">${(al.items || [])
           .map((k) => `<button class="chip clickable" data-actkey="${k}">${k.replace(":", "장 ")}</button>`)
           .join("")}</div>
         ${al.boundary ? `<div class="ifrs-boundary"><span class="boundary-label">연결의 한계</span>${al.boundary}</div>` : ""}
       </div>`
    : "";
  return `
    <h3 class="kics-ex-h">${ex.heading}</h3>
    ${ex.formula ? `<div class="field"><span class="label">산출식</span><div class="formula-text">$$${escapeLatex(ex.formula)}$$</div>${ex.formulaNote ? `<p class="panel-note small">${ex.formulaNote}</p>` : ""}</div>` : ""}
    ${qa ? `<div class="field"><span class="label">핵심 질문</span>${qa}</div>` : ""}
    ${lineage ? `<div class="field"><span class="label">아래로 내려가기 (Lineage)</span><div class="chips">${lineage}</div></div>` : ""}
    ${alHtml}
    <p class="page-ref">근거 — ${ex.sourceLabel}. 위 [해설서 원문] 탭에서 해당 페이지를 직접 확인할 수 있습니다.</p>
  `;
}

function renderIfrsTOC(nav) {
  for (const ch of IFRS.chapters) {
    const chapterEl = document.createElement("div");
    chapterEl.className = "chapter";
    const chTitleEl = document.createElement("div");
    chTitleEl.className = "chapter-title";
    chTitleEl.textContent = `제${ch.num}장 ${ch.title}`;
    const sectionsWrap = document.createElement("div");
    sectionsWrap.className = "sections";

    for (const sec of ch.sections) {
      const secEl = document.createElement("div");
      secEl.className = "section";
      const secTitleEl = document.createElement("div");
      secTitleEl.className = "section-title";
      secTitleEl.innerHTML = `<span class="dot ${sec.general ? "general" : "theory"}"></span><span>${sec.secTitle}</span>`;
      const itemsWrap = document.createElement("div");
      itemsWrap.className = "items";

      for (const item of sec.items) {
        const itemEl = document.createElement("div");
        itemEl.className = "item";
        const label = item.code ? `${item.code} ${item.title}` : item.title;
        itemEl.innerHTML = `<span class="dot ${item.theory ? "theory" : "general"}"></span><span>${label}</span>`;
        itemEl.addEventListener("click", (e) => {
          e.stopPropagation();
          openIfrsItem(ch, sec, item);
          document.querySelectorAll(".item").forEach((n) => n.classList.remove("active"));
          itemEl.classList.add("active");
        });
        itemsWrap.appendChild(itemEl);
      }
      secTitleEl.addEventListener("click", () => itemsWrap.classList.toggle("open"));
      secEl.appendChild(secTitleEl);
      secEl.appendChild(itemsWrap);
      sectionsWrap.appendChild(secEl);
    }
    chTitleEl.addEventListener("click", () => sectionsWrap.classList.toggle("open"));
    chapterEl.appendChild(chTitleEl);
    chapterEl.appendChild(sectionsWrap);
    nav.appendChild(chapterEl);
  }
}

function renderActTOC(nav) {
  for (const ch of ACT.chapters) {
    const chapterEl = document.createElement("div");
    chapterEl.className = "chapter";
    const chTitleEl = document.createElement("div");
    chTitleEl.className = "chapter-title";
    chTitleEl.textContent = `제${ch.num}장 ${ch.title}`;
    const sectionsWrap = document.createElement("div");
    sectionsWrap.className = "sections";

    for (const part of ch.parts) {
      const secEl = document.createElement("div");
      secEl.className = "section";
      const secTitleEl = document.createElement("div");
      secTitleEl.className = "section-title";
      secTitleEl.innerHTML = `<span>${part.label}</span>`;
      const itemsWrap = document.createElement("div");
      itemsWrap.className = "items";

      for (const item of part.items) {
        const itemEl = document.createElement("div");
        itemEl.className = "item";
        itemEl.innerHTML = `<span class="dot ${item.def ? "theory" : "general"}"></span><span>${item.num} ${item.title}</span>`;
        itemEl.addEventListener("click", (e) => {
          e.stopPropagation();
          openActItem(ch, part, item);
          document.querySelectorAll(".item").forEach((n) => n.classList.remove("active"));
          itemEl.classList.add("active");
        });
        itemsWrap.appendChild(itemEl);
      }
      secTitleEl.addEventListener("click", () => itemsWrap.classList.toggle("open"));
      secEl.appendChild(secTitleEl);
      secEl.appendChild(itemsWrap);
      sectionsWrap.appendChild(secEl);
    }
    chTitleEl.addEventListener("click", () => sectionsWrap.classList.toggle("open"));
    chapterEl.appendChild(chTitleEl);
    chapterEl.appendChild(sectionsWrap);
    nav.appendChild(chapterEl);
  }
}

function showWelcome() {
  document.getElementById("welcome").hidden = false;
  document.getElementById("viewer").hidden = true;
}

function imgSrc(pageIndex) {
  return `images/ifrs17/${String(pageIndex).padStart(4, "0")}.jpg`;
}

function renderSourcePane() {
  const total = IFRS.pageCounts.ifrs17;
  currentPage = Math.max(0, Math.min(total - 1, currentPage));
  const wrap = document.getElementById("sourcePane");
  wrap.innerHTML = `
    <div class="pane-header">
      <span>IFRS17 보험회계해설서 원문</span>
      <div class="page-nav">
        <button id="prevBtn">◀ 이전</button>
        <span>${currentPage + 1} / ${total}</span>
        <button id="nextBtn">다음 ▶</button>
      </div>
    </div>
    <div class="page-img-wrap"><img src="${imgSrc(currentPage)}"></div>
  `;
  document.getElementById("prevBtn").addEventListener("click", () => { currentPage -= 1; renderSourcePane(); });
  document.getElementById("nextBtn").addEventListener("click", () => { currentPage += 1; renderSourcePane(); });
}

function openIfrsItem(ch, sec, item) {
  document.getElementById("welcome").hidden = true;
  document.getElementById("viewer").hidden = false;
  document.getElementById("tabBar").hidden = false;
  const label = item.code ? `${item.code} ${item.title}` : item.title;
  document.getElementById("viewerTitle").textContent = `제${ch.num}장 ${ch.title} / ${sec.secTitle} — ${label}`;
  currentPage = item.pageStart;

  const body = document.getElementById("viewerBody");
  let theoryHtml;
  if (item.theory) {
    theoryHtml = `
      <div class="theory-panel">
        <div class="theory-block">
          ${item.code ? `<span class="item-code">${item.code}</span>` : ""}
          <h3>${item.title}</h3>
          <div class="theory-text">${item.theory}</div>
          ${item.connect ? `<div class="connect-box"><span class="label">최신보험수리학과의 연결 (요약)</span>${item.connect}</div>` : ""}
          <p class="jump-hint">※ 공식·도출과정 등 상세 이론은 상단 "최신보험수리학" 모드에서 확인하세요.</p>
        </div>
      </div>
    `;
  } else {
    theoryHtml = `<div class="theory-panel"><div class="general-note">${item.note || "이 절은 최신보험수리학과 직접 대응되는 이론이 없는 일반 회계 영역입니다."}</div></div>`;
  }

  body.innerHTML = `
    <div class="tab-pane active" id="pane-source"><div class="source-viewer" id="sourcePane"></div></div>
    <div class="tab-pane" id="pane-theory">${theoryHtml}</div>
  `;
  renderSourcePane();
  document.querySelectorAll(".tab-btn").forEach((btn) => btn.classList.toggle("active", btn.dataset.tab === "source"));
  wireTabs();
}

// LaTeX source may contain literal < > (comparison operators). Since content is inserted
// via innerHTML, the browser's HTML parser would treat "<X>" as a tag and corrupt it before
// KaTeX ever sees it. Escaping to entities keeps the literal character intact in the DOM text
// node, where KaTeX's auto-render can then read it correctly.
function escapeLatex(s) {
  return String(s).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderDerivation(item) {
  if (item.derivationSteps && item.derivationSteps.length) {
    const stepsHtml = item.derivationSteps.map((s, idx) => `
      <div class="deriv-step">
        ${s.text ? `<div class="deriv-text">${s.text}</div>` : ""}
        ${s.eq ? `<div class="deriv-eq">$$${escapeLatex(s.eq)}$$</div>` : ""}
      </div>
    `).join("");
    return `<div class="derivation-steps">${stepsHtml}</div>${item.derivation ? `<div class="theory-text deriv-summary">${item.derivation}</div>` : ""}`;
  }
  return `<div class="theory-text">${item.derivation}</div>`;
}

const STRENGTH_CLASS = {
  "직접적인 수리적 기반": "s-direct",
  "강한 개념적 연관": "s-strong",
  "간접적 연관": "s-indirect",
  "직접 대응 없음": "s-none",
};

// 연결의 성격 — 수리적 연결과 IFRS17 고유 회계처리를 구분해 표시한다.
// (교재 11~12장처럼 IFRS17 자체를 서술하는 절은 '수리적 기반'이 아니라 회계처리 대응이다)
const NATURE_CLASS = {
  "수리적 기반": "n-math",
  "IFRS17 고유 회계처리": "n-acct",
  "혼합": "n-mixed",
};

// 예제 렌더링. 교재 예제를 옮긴 것이 아니라 이론을 바탕으로 새로 만든 문제이며,
// 모든 수치는 scripts_audit/add_examples_*.py 의 verify() 로 재계산 검증한 값이다.
function renderExamples(item, standalone) {
  const ex = item.examples;
  if (!ex || !ex.length) return standalone ? '<p class="na">이 절의 예제는 아직 준비 중입니다.</p>' : "";
  const blocks = ex
    .map((e, idx) => {
      const given = (e.given || []).map((g) => `<li>${g}</li>`).join("");
      const steps = (e.steps || [])
        .map(
          (s, i) => `<div class="ex-step">
            <div class="ex-step-no">${i + 1}</div>
            <div class="ex-step-body">
              ${s.text ? `<div class="ex-step-text">${s.text}</div>` : ""}
              ${s.eq ? `<div class="ex-step-eq">$$${escapeLatex(s.eq)}$$</div>` : ""}
            </div>
          </div>`
        )
        .join("");
      return `<div class="example">
        <div class="ex-head"><span class="ex-badge">예제 ${ex.length > 1 ? idx + 1 : ""}</span></div>
        <div class="ex-q">${e.q}</div>
        ${given ? `<div class="ex-given"><span class="ex-label">주어진 조건</span><ul>${given}</ul></div>` : ""}
        <div class="ex-sol"><span class="ex-label">풀이</span>${steps}</div>
        ${e.answer ? `<div class="ex-answer"><span class="ex-label">답</span>${e.answer}</div>` : ""}
        ${e.comment ? `<div class="ex-comment">${e.comment}</div>` : ""}
      </div>`;
    })
    .join("");
  return standalone ? blocks : `<div class="field examples-field"><span class="label">⑫ 예제</span>${blocks}</div>`;
}

let ACT_TAB = "theory";
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
        r.cells.map((c) => `<td>${c ? "$" + c + "$" : "—"}</td>`).join("") +
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

function renderMath(el) {
  if (window.renderMathInElement) {
    window.renderMathInElement(el, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
      ],
      throwOnError: false,
    });
  }
}

function wireTabs() {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.onclick = () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".tab-pane").forEach((p) => p.classList.remove("active"));
      document.getElementById(`pane-${btn.dataset.tab}`).classList.add("active");
    };
  });
}

function onSearch(e) {
  const q = e.target.value.trim();
  const nav = document.getElementById("toc");
  if (!q) {
    renderTOC();
    return;
  }
  // 보험사 분석 모드에서는 회사명 검색이므로 목차 렌더러가 직접 필터링한다.
  if (MODE === "company") {
    renderTOC();
    return;
  }
  const results = [];
  if (MODE === "ifrs17") {
    for (const ch of IFRS.chapters) {
      for (const sec of ch.sections) {
        for (const item of sec.items) {
          const hay = [item.title, item.theory, item.connect, item.note].filter(Boolean).join(" ");
          if (hay.includes(q) || sec.secTitle.includes(q)) results.push({ ch, sec, item, kind: "ifrs17" });
        }
      }
    }
  } else if (MODE === "actuary") {
    for (const ch of ACT.chapters) {
      for (const part of ch.parts) {
        for (const item of part.items) {
          const hay = [item.title, item.def, item.formula, item.derivation].filter(Boolean).join(" ");
          if (hay.includes(q)) results.push({ ch, part, item, kind: "actuary" });
        }
      }
    }
  } else {
    for (const ch of KICS.chapters) {
      for (const it of ch.items) {
        const hay = [it.title, it.connect].filter(Boolean).join(" ");
        if (hay.includes(q)) results.push({ ch, item: it, kind: "kics" });
      }
    }
  }
  nav.innerHTML = `<div class="search-results"></div>`;
  const rc = nav.querySelector(".search-results");
  if (results.length === 0) {
    rc.innerHTML = `<div class="no-match">검색 결과가 없습니다.</div>`;
    return;
  }
  for (const r of results) {
    const el = document.createElement("div");
    el.className = "search-result-item";
    if (r.kind === "ifrs17") {
      const label = r.item.code ? `${r.item.code} ${r.item.title}` : r.item.title;
      el.innerHTML = `${label}<div class="path">제${r.ch.num}장 ${r.ch.title} / ${r.sec.secTitle}</div>`;
      el.addEventListener("click", () => openIfrsItem(r.ch, r.sec, r.item));
    } else if (r.kind === "actuary") {
      el.innerHTML = `${r.item.num} ${r.item.title}<div class="path">제${r.ch.num}장 ${r.ch.title} / ${r.part.label}</div>`;
      el.addEventListener("click", () => openActItem(r.ch, r.part, r.item));
    } else {
      el.innerHTML = `${r.item.code}. ${r.item.title}<div class="path">${r.ch.num}. ${r.ch.title}</div>`;
      el.addEventListener("click", () => openKicsItem(r.ch, r.item));
    }
    rc.appendChild(el);
  }
}

init();
