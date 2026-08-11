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

    const titleEl = document.createElement("div");
    titleEl.className = "chapter-title";
    const badge = ch.depth === "deep" ? `<span class="badge deep">정밀매칭</span>` : `<span class="badge brief">개념연결</span>`;
    titleEl.innerHTML = `<span>제${ch.num}장 ${ch.title}</span>${badge}`;

    const sectionsEl = document.createElement("div");
    sectionsEl.className = "sections";
    for (const sec of ch.sections || []) {
      const secEl = document.createElement("div");
      secEl.className = "section-item";
      secEl.textContent = sec.title;
      secEl.addEventListener("click", (e) => {
        e.stopPropagation();
        openSection(ch, sec);
        document.querySelectorAll(".section-item").forEach((n) => n.classList.remove("active"));
        secEl.classList.add("active");
      });
      sectionsEl.appendChild(secEl);
    }

    titleEl.addEventListener("click", () => sectionsEl.classList.toggle("open"));

    chapterEl.appendChild(titleEl);
    chapterEl.appendChild(sectionsEl);
    nav.appendChild(chapterEl);
  }
}

function showWelcome() {
  document.getElementById("welcome").hidden = false;
  document.getElementById("viewer").hidden = true;
}

function imgSrc(pageIndex) {
  const idx = String(pageIndex).padStart(4, "0");
  return `images/ifrs17/${idx}.jpg`;
}

function pageNavHtml(pageIndex, total) {
  return `<div class="page-nav">
    <button class="prev">◀</button>
    <span class="pageLabel">${pageIndex + 1} / ${total}</span>
    <button class="next">▶</button>
  </div>`;
}

function renderIfrs17Pane(container, pageIndex, label) {
  const total = TOC.pageCounts.ifrs17;
  pageIndex = Math.max(0, Math.min(total - 1, pageIndex));
  container.innerHTML = `
    <div class="pane-header">
      <span>${label}</span>
      ${pageNavHtml(pageIndex, total)}
    </div>
    <div class="page-img-wrap">
      <img src="${imgSrc(pageIndex)}">
    </div>
  `;
  const img = container.querySelector("img");
  const pageLabel = container.querySelector(".pageLabel");
  container.querySelector(".prev").addEventListener("click", () => {
    if (pageIndex > 0) {
      pageIndex -= 1;
      img.src = imgSrc(pageIndex);
      pageLabel.textContent = `${pageIndex + 1} / ${total}`;
    }
  });
  container.querySelector(".next").addEventListener("click", () => {
    if (pageIndex < total - 1) {
      pageIndex += 1;
      img.src = imgSrc(pageIndex);
      pageLabel.textContent = `${pageIndex + 1} / ${total}`;
    }
  });
}

function openSection(ch, sec) {
  document.getElementById("welcome").hidden = true;
  const viewer = document.getElementById("viewer");
  viewer.hidden = false;
  document.getElementById("viewerTitle").textContent = `제${ch.num}장 ${ch.title} — ${sec.title}`;

  const body = document.getElementById("viewerBody");
  const refs = sec.refs || [];

  let refsHtml = "";
  if (refs.length === 0) {
    refsHtml = `<div class="no-match">이 절에 대한 IFRS17 해설서 대응 항목이 아직 등록되지 않았습니다.</div>`;
  } else {
    refsHtml = `<ul class="ref-list">` + refs.map((r) => `<li>
        <div><strong>${r.title}</strong> (p.${r.pageLabel || "-"})</div>
        <div class="path">IFRS17 보험회계해설서</div>
      </li>`).join("") + `</ul>`;
  }

  body.innerHTML = `
    <div class="panes">
      <div class="pane left">
        <div class="pane-header"><span>최신보험수리학 — 핵심 이론</span></div>
        <div class="theory-box">${sec.theory || "이론 요약이 아직 작성되지 않았습니다."}</div>
      </div>
      <div class="pane right">
        <div class="pane-header"><span>대응하는 IFRS17 해설서 절</span></div>
        ${refsHtml}
        ${refs.length ? `<div id="rightImgPane"></div>` : ""}
        ${sec.note ? `<div class="explain-box"><h4>연결 설명</h4>${sec.note}</div>` : ""}
      </div>
    </div>
  `;

  if (refs.length) {
    renderIfrs17Pane(document.getElementById("rightImgPane"), refs[0].pageStart, refs[0].title);
  }
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
    for (const sec of ch.sections || []) {
      if (sec.title.includes(q) || (sec.note && sec.note.includes(q)) || (sec.theory && sec.theory.includes(q))) {
        results.push({ ch, sec });
      }
    }
  }
  nav.innerHTML = `<div class="search-results"></div>`;
  const rc = nav.querySelector(".search-results");
  if (results.length === 0) {
    rc.innerHTML = `<div class="no-match">검색 결과가 없습니다.</div>`;
    return;
  }
  for (const { ch, sec } of results) {
    const el = document.createElement("div");
    el.className = "search-result-item";
    el.innerHTML = `${sec.title}<div class="path">제${ch.num}장 ${ch.title}</div>`;
    el.addEventListener("click", () => openSection(ch, sec));
    rc.appendChild(el);
  }
}

init();
