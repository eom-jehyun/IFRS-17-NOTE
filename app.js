let TOC = null;

async function init() {
  const tocRes = await fetch("data/toc.json");
  TOC = await tocRes.json();
  renderTOC();
  document.getElementById("search").addEventListener("input", onSearch);
  document.getElementById("backBtn").addEventListener("click", showWelcome);
}

function renderTOC() {
  const nav = document.getElementById("toc");
  nav.innerHTML = "";
  for (const ch of TOC.chapters) {
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
          openItem(ch, sec, item);
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

let currentPage = 0;

function renderSourcePane() {
  const total = TOC.pageCounts.ifrs17;
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

function openItem(ch, sec, item) {
  document.getElementById("welcome").hidden = true;
  const viewer = document.getElementById("viewer");
  viewer.hidden = false;
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
          ${item.connect ? `<div class="connect-box"><span class="label">최신보험수리학과의 연결</span>${item.connect}</div>` : ""}
        </div>
      </div>
    `;
  } else {
    theoryHtml = `
      <div class="theory-panel">
        <div class="general-note">${item.note || "이 절은 최신보험수리학과 직접 대응되는 이론이 없는 일반 회계 영역입니다."}</div>
      </div>
    `;
  }

  body.innerHTML = `
    <div class="tab-pane active" id="pane-source">
      <div class="source-viewer" id="sourcePane"></div>
    </div>
    <div class="tab-pane" id="pane-theory">${theoryHtml}</div>
  `;
  renderSourcePane();

  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === "source");
  });
  wireTabs();
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
  for (const ch of TOC.chapters) {
    for (const sec of ch.sections) {
      for (const item of sec.items) {
        const hay = [item.title, item.theory, item.connect, item.note].filter(Boolean).join(" ");
        if (hay.includes(q) || sec.secTitle.includes(q)) {
          results.push({ ch, sec, item });
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
  for (const { ch, sec, item } of results) {
    const el = document.createElement("div");
    el.className = "search-result-item";
    const label = item.code ? `${item.code} ${item.title}` : item.title;
    el.innerHTML = `${label}<div class="path">제${ch.num}장 ${ch.title} / ${sec.secTitle}</div>`;
    el.addEventListener("click", () => openItem(ch, sec, item));
    rc.appendChild(el);
  }
}

init();
