let IFRS = null;
let ACT = null;
let MODE = "ifrs17"; // "ifrs17" | "actuary"
let currentPage = 0;

async function init() {
  const [ifrsRes, actRes] = await Promise.all([fetch("data/toc.json"), fetch("data/actuary.json")]);
  IFRS = await ifrsRes.json();
  ACT = await actRes.json();

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

  if (mode === "ifrs17") {
    document.getElementById("sidebarTitle").textContent = "IFRS17 보험회계해설서";
    document.getElementById("sidebarSubtitle").textContent = "↔ 최신보험수리학 이론 연계";
    document.getElementById("welcomeTitle").textContent = "왼쪽 목차에서 IFRS17 보험회계해설서의 장·절을 선택하세요.";
    document.getElementById("welcomeIfrs17").hidden = false;
    document.getElementById("welcomeActuary").hidden = true;
    document.getElementById("tabBar").hidden = false;
  } else {
    document.getElementById("sidebarTitle").textContent = "최신보험수리학";
    document.getElementById("sidebarSubtitle").textContent = "↔ IFRS17 보험회계해설서 연계";
    document.getElementById("welcomeTitle").textContent = "왼쪽 목차에서 최신보험수리학의 장·절을 선택하세요.";
    document.getElementById("welcomeIfrs17").hidden = true;
    document.getElementById("welcomeActuary").hidden = false;
    document.getElementById("tabBar").hidden = true;
  }
  showWelcome();
  renderTOC();
}

function renderTOC() {
  const nav = document.getElementById("toc");
  nav.innerHTML = "";
  if (MODE === "ifrs17") renderIfrsTOC(nav);
  else renderActTOC(nav);
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

function openActItem(ch, part, item) {
  document.getElementById("welcome").hidden = true;
  document.getElementById("viewer").hidden = false;
  document.getElementById("tabBar").hidden = true;
  document.getElementById("viewerTitle").textContent = `제${ch.num}장 ${ch.title} / ${part.label} — ${item.num} ${item.title}`;

  const body = document.getElementById("viewerBody");
  let html;
  if (item.def) {
    html = `
      <div class="theory-panel">
        <div class="theory-block">
          <span class="item-code">${item.num}</span>
          <h3>${item.title}</h3>
          <div class="def-box"><span class="label">정의</span><div class="theory-text">${item.def}</div></div>
          <div class="formula-box"><span class="label">핵심 공식</span><div class="formula-text">${item.formula}</div></div>
          <div class="derivation-box"><span class="label">도출과정</span><div class="theory-text">${item.derivation}</div></div>
          ${item.related ? `<div class="connect-box"><span class="label">관련 IFRS17 해설서</span>${item.related.join(", ")}</div>` : ""}
          <p class="page-ref">최신보험수리학 p.${item.page} 내용을 기반으로 필자가 재정리</p>
        </div>
      </div>
    `;
  } else {
    html = `
      <div class="theory-panel">
        <div class="general-note">이 항목은 아직 작성 중입니다 (책 목차 순서대로 순차 작성). 곧 정의·핵심공식·도출과정이 채워질 예정입니다. — 최신보험수리학 p.${item.page}</div>
      </div>
    `;
  }
  body.innerHTML = `<div class="tab-pane active">${html}</div>`;
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
  } else {
    for (const ch of ACT.chapters) {
      for (const part of ch.parts) {
        for (const item of part.items) {
          const hay = [item.title, item.def, item.formula, item.derivation].filter(Boolean).join(" ");
          if (hay.includes(q)) results.push({ ch, part, item, kind: "actuary" });
        }
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
    } else {
      el.innerHTML = `${r.item.num} ${r.item.title}<div class="path">제${r.ch.num}장 ${r.ch.title} / ${r.part.label}</div>`;
      el.addEventListener("click", () => openActItem(r.ch, r.part, r.item));
    }
    rc.appendChild(el);
  }
}

init();
