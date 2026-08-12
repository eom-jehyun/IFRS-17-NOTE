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
  const theoryHtml = it.connect
    ? `<div class="theory-panel"><div class="theory-block">
         <div class="connect-box"><span class="label">최신보험수리학과의 연결</span>${it.connect}</div>
       </div></div>`
    : `<div class="theory-panel"><div class="general-note">이 절은 최신보험수리학과 직접 대응되는 이론이 없는 일반 금융·회계 영역입니다.</div></div>`;

  body.innerHTML = `
    <div class="tab-pane active" id="pane-source"><div class="source-viewer" id="sourcePane"></div></div>
    <div class="tab-pane" id="pane-theory">${theoryHtml}</div>
  `;
  renderKicsSourcePane();
  document.querySelectorAll(".tab-btn").forEach((btn) => btn.classList.toggle("active", btn.dataset.tab === "source"));
  wireTabs();
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

function openActItem(ch, part, item) {
  document.getElementById("welcome").hidden = true;
  document.getElementById("viewer").hidden = false;
  document.getElementById("tabBar").hidden = true;
  document.getElementById("viewerTitle").textContent = `제${ch.num}장 ${ch.title} / ${part.label} — ${item.num} ${item.title}`;

  const body = document.getElementById("viewerBody");
  let html;

  if (item.symbols) {
    // full 12-field schema
    const symbolsHtml = item.symbols.map((s) => `<li><span class="sym">${s.sym}</span> — ${s.meaning}</li>`).join("");
    const assumptionsHtml = (item.assumptions || []).map((a) => `<li>${a}</li>`).join("");
    const termsHtml = (item.termMeanings || []).map((t) => `<li><span class="sym">${t.term}</span> — ${t.meaning}</li>`).join("");
    const prereqHtml = (item.prerequisites || []).map((p) => `<span class="chip">${p}</span>`).join("");
    const leadsHtml = (item.leadsTo || []).map((p) => `<span class="chip">${p}</span>`).join("");
    const ifrs = item.ifrs17 || { strength: "직접 대응 없음" };
    const strengthClass = STRENGTH_CLASS[ifrs.strength] || "s-none";

    html = `
      <div class="theory-panel">
        <div class="theory-block">
          <span class="item-code">${item.num}</span>
          <h3>${item.title}${item.titleEn ? ` <span class="title-en">(${item.titleEn})</span>` : ""}</h3>

          <div class="field"><span class="label">① 정의</span><div class="theory-text">${item.def}</div></div>

          ${symbolsHtml ? `<div class="field"><span class="label">② 기호</span><ul class="symbol-list">${symbolsHtml}</ul></div>` : ""}

          ${assumptionsHtml ? `<div class="field"><span class="label">③ 전제(가정)</span><ul class="plain-list">${assumptionsHtml}</ul></div>` : ""}

          <div class="field"><span class="label">④ 핵심 공식</span><div class="formula-text">$$${escapeLatex(item.formula)}$$</div></div>

          <div class="field"><span class="label">⑤ 수식의 도출</span>${renderDerivation(item)}</div>

          ${termsHtml ? `<div class="field"><span class="label">⑥ 각 항의 의미</span><ul class="symbol-list">${termsHtml}</ul></div>` : ""}

          ${item.intuition ? `<div class="field"><span class="label">⑦ 직관</span><div class="theory-text">${item.intuition}</div></div>` : ""}

          ${item.relatedFormulas ? `<div class="field"><span class="label">⑧ 관련 공식</span><div class="theory-text">${item.relatedFormulas}</div></div>` : ""}

          ${prereqHtml ? `<div class="field"><span class="label">⑨ 선수개념</span><div class="chips">${prereqHtml}</div></div>` : ""}
          ${leadsHtml ? `<div class="field"><span class="label">⑩ 다음 개념</span><div class="chips">${leadsHtml}</div></div>` : ""}

          <div class="field ifrs-field">
            <span class="label">⑪ IFRS17 연결</span>
            <div class="ifrs-strength ${strengthClass}">${ifrs.strength}</div>
            ${ifrs.items && ifrs.items.length ? `<ul class="plain-list">${ifrs.items.map((i) => `<li>${i}</li>`).join("")}</ul>` : ""}
            ${ifrs.note ? `<div class="ifrs-note">${ifrs.note}</div>` : ""}
          </div>

          <p class="page-ref">출처 — 『최신보험수리학』 제${ch.num}장 ${ch.title} ${part.label}, p.${item.page} 내용을 참고하여 필자가 재구성 (원문 문장 인용 아님)</p>
        </div>
      </div>
    `;
  } else if (item.def) {
    // legacy 3-field schema (not yet upgraded to full spec)
    html = `
      <div class="theory-panel">
        <div class="theory-block">
          <span class="item-code">${item.num}</span>
          <h3>${item.title}</h3>
          <div class="field"><span class="label">정의</span><div class="theory-text">${item.def}</div></div>
          <div class="field"><span class="label">핵심 공식</span><div class="formula-text">$$${escapeLatex(item.formula)}$$</div></div>
          <div class="field"><span class="label">도출과정</span><div class="theory-text">${item.derivation}</div></div>
          ${item.related ? `<div class="connect-box"><span class="label">관련 IFRS17 해설서</span>${item.related.join(", ")}</div>` : ""}
          <p class="page-ref">최신보험수리학 p.${item.page} 내용을 필자가 이해하여 재정리 (원문 인용 아님) · 상세 스키마 업그레이드 예정</p>
        </div>
      </div>
    `;
  } else {
    html = `
      <div class="theory-panel">
        <div class="general-note">이 항목은 아직 작성 중입니다 (책 목차 순서대로 순차 작성). — 최신보험수리학 p.${item.page}</div>
      </div>
    `;
  }
  body.innerHTML = `<div class="tab-pane active">${html}</div>`;
  renderMath(body);
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
