// ─────────────────────────────────────────────────────────────────────────────
// 보험사 분석 모드
//
// 이 모드의 목적은 DART 재무검색이 아니다. 실제 보험회사의 공시 숫자에서 출발해
//   실제 숫자 → IFRS17/K-ICS 기준 → 보험수리적 원리
// 로 내려갈 수 있게 만드는 것이 목적이며, 기존 3개 모드(해설서·보험수리학·K-ICS)의
// 콘텐츠로 이동하는 진입점 역할을 한다.
//
// API Key는 이 파일에 존재하지 않는다. 브라우저 → Vercel 서버리스 함수 → OpenDART 구조이며,
// 키는 Vercel 환경변수(DART_API_KEY)에만 존재한다.
// ─────────────────────────────────────────────────────────────────────────────

// 백엔드 주소는 config.js 한 곳에서만 관리한다(중복 하드코딩 금지).
const API_BASE = SITE_CONFIG.apiBase();

let MAPPING = null;
let COMPANIES = null;
let CURRENT_CO = null;
let COMPANY_TAB = "ifrs17";
// 같은 회사를 다시 눌렀을 때 재요청하지 않도록 캐시한다 (lazy loading + cache)
const CACHE = { ifrs17: {}, kics: {} };

async function loadMapping() {
  if (MAPPING) return MAPPING;
  MAPPING = await (await fetch("data/dart-mapping.json")).json();
  return MAPPING;
}

/** 서버에서 보험사 목록을 받아오되, 실패하면 정적 폴백 목록을 쓴다(백엔드 미배포 상황 대비). */
async function loadCompanies() {
  if (COMPANIES) return COMPANIES;
  try {
    const res = await fetch(`${API_BASE}/companies`);
    if (!res.ok) throw new Error(String(res.status));
    COMPANIES = (await res.json()).companies;
  } catch (e) {
    COMPANIES = FALLBACK_INSURERS;
    BACKEND_DOWN = true;
  }
  return COMPANIES;
}

let BACKEND_DOWN = false;

// 백엔드가 아직 배포되지 않아도 목록과 안내는 보이도록 하는 폴백.
// api/lib/insurers.js 와 동일한 내용이며, 실제 조회는 백엔드가 있어야 동작한다.
const FALLBACK_INSURERS = [
  { corpCode: "00126256", stockCode: "032830", name: "삼성생명", type: "life" },
  { corpCode: "00113058", stockCode: "088350", name: "한화생명", type: "life" },
  { corpCode: "00117267", stockCode: "082640", name: "동양생명", type: "life" },
  { corpCode: "00112332", stockCode: "085620", name: "미래에셋생명", type: "life" },
  { corpCode: "00139214", stockCode: "000810", name: "삼성화재해상보험", type: "nonlife" },
  { corpCode: "00159102", stockCode: "005830", name: "DB손해보험", type: "nonlife" },
  { corpCode: "00164973", stockCode: "001450", name: "현대해상화재보험", type: "nonlife" },
  { corpCode: "00120216", stockCode: "002550", name: "KB손해보험", type: "nonlife" },
  { corpCode: "00117744", stockCode: "000060", name: "메리츠화재해상보험", type: "nonlife" },
  { corpCode: "00135917", stockCode: "000370", name: "한화손해보험", type: "nonlife" },
  { corpCode: "00113562", stockCode: "000400", name: "롯데손해보험", type: "nonlife" },
  { corpCode: "00103176", stockCode: "000540", name: "흥국화재", type: "nonlife" },
];

async function renderCompanyTOC(nav) {
  await loadMapping();
  const list = await loadCompanies();
  const q = document.getElementById("search").value.trim();
  const shown = q ? list.filter((c) => c.name.includes(q)) : list;

  const groups = [
    ["생명보험", shown.filter((c) => c.type === "life")],
    ["손해보험", shown.filter((c) => c.type === "nonlife")],
  ];

  if (BACKEND_DOWN) {
    const warn = document.createElement("div");
    warn.className = "backend-warn";
    warn.textContent = "DART 백엔드에 연결할 수 없습니다. 회사 목록만 표시되며 실제 조회는 되지 않습니다.";
    nav.appendChild(warn);
  }

  for (const [label, arr] of groups) {
    if (!arr.length) continue;
    const chapterEl = document.createElement("div");
    chapterEl.className = "chapter";
    const t = document.createElement("div");
    t.className = "chapter-title";
    t.textContent = label;
    const wrap = document.createElement("div");
    wrap.className = "sections open";

    for (const co of arr) {
      const el = document.createElement("div");
      el.className = "item";
      el.innerHTML = `<span class="dot theory"></span><span>${co.name}<span class="co-code"> ${co.stockCode}</span></span>`;
      el.addEventListener("click", (e) => {
        e.stopPropagation();
        openCompany(co);
        document.querySelectorAll(".item").forEach((n) => n.classList.remove("active"));
        el.classList.add("active");
      });
      wrap.appendChild(el);
    }
    t.addEventListener("click", () => wrap.classList.toggle("open"));
    chapterEl.appendChild(t);
    chapterEl.appendChild(wrap);
    nav.appendChild(chapterEl);
  }
}

function openCompany(co) {
  CURRENT_CO = co;
  COMPANY_TAB = "ifrs17";
  document.getElementById("welcome").hidden = true;
  document.getElementById("viewer").hidden = false;
  document.getElementById("tabBar").hidden = true;
  document.getElementById("viewerTitle").textContent = `${co.name}`;
  renderCompanyView();
}

function renderCompanyView() {
  const body = document.getElementById("viewerBody");
  const co = CURRENT_CO;
  body.innerHTML = `
    <div class="co-head">
      <div class="co-title">${co.name}</div>
      <div class="co-meta">
        <span>DART 고유번호 <b>${co.corpCode}</b></span>
        <span>종목코드 <b>${co.stockCode}</b></span>
        <span>${co.type === "life" ? "생명보험" : "손해보험"}</span>
      </div>
    </div>
    <div class="co-tabs">
      ${["ifrs17", "kics", "source"]
        .map(
          (t) =>
            `<button class="co-tab ${COMPANY_TAB === t ? "active" : ""}" data-cotab="${t}">${
              { ifrs17: "IFRS17", kics: "K-ICS", source: "출처 / 원문" }[t]
            }</button>`
        )
        .join("")}
    </div>
    <div id="coPanel" class="co-panel"><div class="loading">조회 중…</div></div>
  `;
  body.querySelectorAll(".co-tab").forEach((b) =>
    b.addEventListener("click", () => {
      COMPANY_TAB = b.dataset.cotab;
      renderCompanyView();
    })
  );
  if (COMPANY_TAB === "ifrs17") loadIfrsPanel();
  else if (COMPANY_TAB === "kics") loadKicsPanel();
  else loadSourcePanel();
}

// 공시 원화 금액 표시.
// 억원으로 반올림하면 소액(예: 삼성화재 보험계약자산 12,291,509원)이 "0 억원"으로 보여
// '실제 값 0'(재보험계약부채)과 구분되지 않는다. 따라서 크기에 따라 단위를 바꾸고,
// 정확히 0인 경우만 "0"으로 표시한다.
function fmtAmount(n) {
  if (n === null || n === undefined) return null;
  if (n === 0) return `<span class="zero">0</span> <span class="unit">(공시값 0)</span>`;
  const abs = Math.abs(n);
  if (abs >= 1e8) {
    return (n / 1e8).toLocaleString("ko-KR", { maximumFractionDigits: 0 }) + ' <span class="unit">억원</span>';
  }
  if (abs >= 1e4) {
    return (n / 1e4).toLocaleString("ko-KR", { maximumFractionDigits: 0 }) + ' <span class="unit">만원</span>';
  }
  return n.toLocaleString("ko-KR") + ' <span class="unit">원</span>';
}

function fmtDiff(v) {
  if (v === null || v === undefined) return `<span class="na">—</span>`;
  const sign = v > 0 ? "+" : "";
  const cls = v > 0 ? "up" : v < 0 ? "down" : "";
  return `<span class="${cls}">${sign}${(v / 1e8).toLocaleString("ko-KR", { maximumFractionDigits: 0 })}</span>`;
}

function fmtPct(v) {
  if (v === null || v === undefined) return `<span class="na">—</span>`;
  const sign = v > 0 ? "+" : "";
  const cls = v > 0 ? "up" : v < 0 ? "down" : "";
  return `<span class="${cls}">${sign}${v.toFixed(1)}%</span>`;
}

async function loadIfrsPanel() {
  const panel = document.getElementById("coPanel");
  const co = CURRENT_CO;
  let data = CACHE.ifrs17[co.corpCode];
  if (!data) {
    try {
      const res = await fetch(`${API_BASE}/ifrs17?corpCode=${co.corpCode}`);
      data = await res.json();
      CACHE.ifrs17[co.corpCode] = data;
    } catch (e) {
      panel.innerHTML = `<div class="err">DART 조회 중 오류 발생 — 백엔드에 연결할 수 없습니다. (${e.message})</div>`;
      return;
    }
  }
  if (data.error) {
    panel.innerHTML = `<div class="err">${data.error}</div>`;
    return;
  }

  const years = data.years || [];
  const head = years.map((y) => `<th>${y.bsnsYear}<span class="fsdiv">${y.fsDiv}</span></th>`).join("");

  const bsRows = (data.balanceSheet || [])
    .map((row) => {
      const cells = row.values
        .map((v) => `<td>${v.amount === null ? `<span class="na">${v.status}</span>` : fmtAmount(v.amount)}</td>`)
        .join("");
      const latest = row.values[0] || {};
      return `<tr>
        <td class="acct"><button class="acct-link" data-acct="${row.label}">${row.label}</button></td>
        ${cells}
        <td class="diff">${fmtDiff(latest.diffFromPrevYear)}</td>
        <td class="diff">${fmtPct(latest.pctChangeFromPrevYear)}</td>
      </tr>`;
    })
    .join("");

  const isRow = (row) => {
    const cells = row.values
      .map((v) => `<td>${v.amount === null ? `<span class="na">${v.status}</span>` : fmtAmount(v.amount)}</td>`)
      .join("");
    const latest = row.values[0] || {};
    return `<tr>
      <td class="acct"><button class="acct-link" data-acct="${row.accountName}">${row.accountName}</button>${
      row.legacyIfrs4 ? `<span class="legacy-badge">IFRS4 비교계정</span>` : ""
    }</td>
      ${cells}
      <td class="diff">${fmtDiff(latest.diffFromPrevYear)}</td>
      <td class="diff">${fmtPct(latest.pctChangeFromPrevYear)}</td>
    </tr>`;
  };

  const current = (data.incomeStatement || []).filter((r) => !r.legacyIfrs4);
  const legacy = (data.incomeStatement || []).filter((r) => r.legacyIfrs4);
  const isRows = current.map(isRow).join("");
  const legacyRows = legacy.map(isRow).join("");

  panel.innerHTML = `
    <p class="panel-note">금액 단위는 억원이며, 증감·증감률은 가장 최근 연도와 그 전년도를 비교한 값입니다.
    전년도 금액이 0이거나 계정이 없으면 증감률을 계산하지 않고 <span class="na">—</span>로 표시합니다.
    계정명을 누르면 그 계정이 어떤 기준·어떤 수리적 원리에서 나온 숫자인지로 이동합니다.</p>

    <h4 class="sec-h">재무상태표 — IFRS17 보험계약 관련 계정</h4>
    <div class="table-scroll"><table class="fin-table">
      <thead><tr><th>계정</th>${head}<th>증감</th><th>증감률</th></tr></thead>
      <tbody>${bsRows || `<tr><td colspan="9" class="na">계정 확인 불가</td></tr>`}</tbody>
    </table></div>

    <h4 class="sec-h">손익계산서 — 보험 관련 계정 (공시된 계정명 그대로)</h4>
    <p class="panel-note small">손익계산서 계정명은 회사마다 다르고, 같은 회사에서도 연도별로 달라질 수 있습니다
    (예: 생보사 '보험서비스수익' vs 손보사 '보험수익'). 사이트가 임의로 이름을 통일하지 않고 공시된 원래
    계정명을 그대로 보여주며, 특정 연도에 그 이름이 없으면 '해당 연도 미공시 또는 계정 확인 불가'로 표시합니다.
    따라서 같은 행의 빈칸이 반드시 '금액 0'을 뜻하지는 않습니다.</p>
    <div class="table-scroll"><table class="fin-table">
      <thead><tr><th>계정</th>${head}<th>증감</th><th>증감률</th></tr></thead>
      <tbody>${isRows || `<tr><td colspan="9" class="na">계정 확인 불가</td></tr>`}</tbody>
    </table></div>

    ${legacyRows
      ? `<h4 class="sec-h">참고 — 과거 IFRS4 기준 비교계정</h4>
         <p class="panel-note small">이 회사는 IFRS17 계정과 함께 과거 IFRS4 기준 계정을 비교표시로 함께 공시했습니다.
         IFRS17 계정이 아니므로 위 표와 합산하거나 같은 개념으로 비교하면 안 됩니다.
         두 기준의 차이는 보험수리학 12장 I-5(IFRS4와 IFRS17의 손익인식 비교)에서 다룹니다.</p>
         <div class="table-scroll"><table class="fin-table">
           <thead><tr><th>계정</th>${head}<th>증감</th><th>증감률</th></tr></thead>
           <tbody>${legacyRows}</tbody>
         </table></div>`
      : ""}

    <div id="acctDetail"></div>
  `;
  panel.querySelectorAll(".acct-link").forEach((b) =>
    b.addEventListener("click", () => showAccountBridge(b.dataset.acct))
  );
}

/** 실제 계정 → 해설서 절 → 보험수리학 이론으로 내려가는 연결 패널 */
function showAccountBridge(accountName) {
  const box = document.getElementById("acctDetail");
  const m = MAPPING.exact[accountName] || MAPPING.keyword.find((k) => k.match.some((s) => accountName.includes(s)));

  if (!m) {
    box.innerHTML = `<div class="bridge-card">
      <h4>${accountName}</h4>
      <p class="na">이 계정에 대해 확인된 해설서·보험수리학 연결이 아직 없습니다. 억지로 연결하지 않고 비워 둡니다.</p>
    </div>`;
    box.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }

  const ifrsLinks = (m.ifrs17 || [])
    .map((id) => {
      const found = findIfrsById(id);
      if (!found) return "";
      return `<button class="chip clickable" data-ifrsid="${id}">${found.item.code ? found.item.code + " " : ""}${found.item.title} <span class="pg">p.${found.item.pageStart}</span></button>`;
    })
    .join("");

  const actLinks = (m.actuarial || [])
    .map((key) => {
      const found = findActByKey(key);
      if (!found) return "";
      return `<button class="chip clickable" data-actkey="${key}">${found.ch.num}장 ${found.item.num} ${found.item.title}</button>`;
    })
    .join("");

  box.innerHTML = `
    <div class="bridge-card">
      <h4>${accountName}${m.label ? ` <span class="title-en">(${m.label})</span>` : ""}</h4>
      <div class="field"><span class="label">이 계정은 무엇인가</span><div class="theory-text">${m.what}</div></div>
      ${m.whyItMoves ? `<div class="field"><span class="label">왜 이 숫자가 움직이는가</span><div class="theory-text">${m.whyItMoves}</div></div>` : ""}
      ${m.caution ? `<div class="ifrs-boundary"><span class="boundary-label">해석 시 주의</span>${m.caution}</div>` : ""}
      ${m.readingOrder ? `<div class="field"><span class="label">읽는 순서</span><div class="theory-text">${m.readingOrder}</div></div>` : ""}
      ${ifrsLinks ? `<div class="field"><span class="label">보험회계해설서에서 확인하기</span><div class="chips">${ifrsLinks}</div></div>` : ""}
      ${actLinks ? `<div class="field"><span class="label">그 아래의 보험수리학 원리</span><div class="chips">${actLinks}</div></div>` : `<div class="field"><span class="label">그 아래의 보험수리학 원리</span><p class="na">이 계정에 직접 대응하는 보험수리학 이론절이 확인되지 않아 비워 둡니다.</p></div>`}
    </div>
  `;
  box.querySelectorAll("[data-ifrsid]").forEach((b) =>
    b.addEventListener("click", () => jumpToIfrs(b.dataset.ifrsid))
  );
  box.querySelectorAll("[data-actkey]").forEach((b) =>
    b.addEventListener("click", () => jumpToAct(b.dataset.actkey))
  );
  box.scrollIntoView({ behavior: "smooth", block: "start" });
}

function findIfrsById(id) {
  for (const ch of IFRS.chapters)
    for (const sec of ch.sections)
      for (const item of sec.items) if (item.id === id) return { ch, sec, item };
  return null;
}

function findActByKey(key) {
  const [chNum, num] = key.split(":");
  for (const ch of ACT.chapters)
    for (const part of ch.parts)
      for (const item of part.items)
        if (String(ch.num) === chNum && item.num === num) return { ch, part, item };
  return null;
}

function jumpToIfrs(id) {
  const found = findIfrsById(id);
  if (!found) return;
  switchMode("ifrs17");
  openIfrsItem(found.ch, found.sec, found.item);
}

function jumpToAct(key) {
  const found = findActByKey(key);
  if (!found) return;
  switchMode("actuary");
  openActItem(found.ch, found.part, found.item);
}

async function loadKicsPanel() {
  const panel = document.getElementById("coPanel");
  const co = CURRENT_CO;
  let data = CACHE.kics[co.corpCode];
  if (!data) {
    panel.innerHTML = `<div class="loading">사업보고서 원문에서 지급여력비율 표를 찾는 중… (문서를 내려받아 파싱하므로 다소 걸립니다)</div>`;
    try {
      const res = await fetch(`${API_BASE}/kics?corpCode=${co.corpCode}`);
      data = await res.json();
      CACHE.kics[co.corpCode] = data;
    } catch (e) {
      panel.innerHTML = `<div class="err">DART 조회 중 오류 발생 (${e.message})</div>`;
      return;
    }
  }
  if (data.error) {
    panel.innerHTML = `<div class="err">${data.error}</div>`;
    return;
  }

  const reports = (data.reports || [])
    .map((r) => {
      if (!r.kicsCandidates.length) {
        return `<div class="kics-report">
          <div class="kics-rep-head">${r.reportName}
            <a class="dart-link" href="${r.dartOriginalUrl}" target="_blank" rel="noopener">DART 원문</a></div>
          <p class="na">${r.unavailable ? r.note : "공시에서 K-ICS 정보 확인 불가"}</p>
        </div>`;
      }
      const cands = r.kicsCandidates.map((c, i) => renderKicsCandidate(c, i, r.kicsCandidates.length)).join("");
      return `<div class="kics-report">
        <div class="kics-rep-head">${r.reportName}
          <a class="dart-link" href="${r.dartOriginalUrl}" target="_blank" rel="noopener">DART 원문</a></div>
        <p class="panel-note small">${r.note}</p>
        ${cands}
      </div>`;
    })
    .join("");

  panel.innerHTML = `
    <p class="panel-note">${data.methodologyNote}</p>
    <div class="ifrs-boundary"><span class="boundary-label">이 화면이 하지 않는 것</span>
      일반 재무상태표로부터 K-ICS 비율을 계산하거나 추정하지 않습니다. 회사가 공시한 표에서 읽어온 값만 표시하며,
      공시되지 않은 값은 빈칸으로 남깁니다. 비율 변동의 원인도 산술적으로 분해 가능한 범위까지만 서술하고,
      금리·주가 등 외부요인을 원인으로 단정하지 않습니다.</div>
    ${reports || `<p class="na">최근 사업보고서를 찾을 수 없습니다.</p>`}
    ${renderKicsTheoryLinks()}
  `;
  panel.querySelectorAll("[data-kicsch]").forEach((b) =>
    b.addEventListener("click", () => {
      const ch = KICS.chapters.find((c) => c.num === b.dataset.kicsch);
      if (ch) {
        switchMode("kics");
        openKicsItem(ch, ch.items[0]);
      }
    })
  );
}

function parseNum(s) {
  if (s === null || s === undefined) return null;
  const t = String(s).trim();
  if (!/^-?[\d,]+(\.\d+)?$/.test(t)) return null;
  return Number(t.replace(/,/g, ""));
}

// 단위는 회사마다 다르다(실측: 삼성생명·DB손해보험은 백만원, 삼성화재는 억원).
// 보고서 표 바로 앞의 "(단위 : ...)" 표기를 찾아 그대로 보여주고, 못 찾으면 단정하지 않는다.
function renderUnitNote(c) {
  const m = (c.contextBefore || "").match(/\(\s*단위\s*[:：][^)]*\)/g);
  if (m && m.length) {
    return `공시 원문에 표시된 단위: <b>${m[m.length - 1]}</b> — 표의 숫자는 가공 없이 그대로 옮긴 값입니다.`;
  }
  return (
    "표의 숫자는 공시 원문을 가공 없이 그대로 옮긴 값입니다. 단위는 회사마다 백만원 또는 억원 등으로 " +
    "다르게 표기되므로, 정확한 단위는 아래 DART 원문 표의 단위 표기를 확인하세요."
  );
}

function renderKicsCandidate(c, idx, total) {
  const header = c.header || [];
  const cols = header.slice(1);

  // 가용자본 행에 '공시 예정' 같은 문자열이 들어가면 셀이 한 칸 밀리므로,
  // 각 행의 데이터 셀 개수를 헤더와 맞추지 않고 있는 그대로 표시한다(임의 정렬 금지).
  const rowHtml = (label, row) =>
    `<tr><td class="acct">${row[0]}</td>${row
      .slice(1)
      .map((v) => `<td>${parseNum(v) === null ? `<span class="na">${v || "—"}</span>` : Number(parseNum(v)).toLocaleString("ko-KR")}</td>`)
      .join("")}</tr>`;

  // 검산: 공시된 가용자본/요구자본으로 비율을 다시 계산해 공시 비율과 비교
  const checks = [];
  const av = c.availableCapitalRow || [];
  const rq = c.requiredCapitalRow || [];
  const rt = c.ratioRow || [];
  const n = Math.max(av.length, rq.length, rt.length);
  for (let k = 1; k < n; k++) {
    const a = parseNum(av[k]);
    const b = parseNum(rq[k]);
    const disclosed = parseNum(rt[k]);
    if (a === null || b === null || b === 0 || disclosed === null) continue;
    const calc = (a / b) * 100;
    const gap = Math.abs(calc - disclosed);
    checks.push({ col: k, calc, disclosed, gap });
  }
  const checkHtml = checks.length
    ? `<table class="fin-table small"><thead><tr><th>구분</th><th>공시 비율</th><th>사이트 검산값 (A/B×100)</th><th>차이</th></tr></thead><tbody>
        ${checks
          .map(
            (ck) =>
              `<tr><td class="acct">${(header[ck.col] || `열 ${ck.col}`)}</td><td>${ck.disclosed.toFixed(1)}%</td><td>${ck.calc.toFixed(1)}%</td><td>${
                ck.gap <= 1
                  ? `<span class="ok">${ck.gap.toFixed(1)}%p (반올림 범위)</span>`
                  : `<span class="warn-txt">${ck.gap.toFixed(1)}%p — 단위 또는 세부 조정 확인 필요</span>`
              }</td></tr>`
          )
          .join("")}
      </tbody></table>`
    : `<p class="na small">검산 가능한 (가용자본, 요구자본, 비율) 3개 값이 모두 공시된 열이 없습니다.</p>`;

  // 비율 변화의 산술적 분해 (인과관계 단정 금지)
  const decomp = [];
  for (let k = 1; k + 1 < n; k++) {
    const a0 = parseNum(av[k + 1]), a1 = parseNum(av[k]);
    const b0 = parseNum(rq[k + 1]), b1 = parseNum(rq[k]);
    const r0 = parseNum(rt[k + 1]), r1 = parseNum(rt[k]);
    if ([a0, a1, b0, b1, r0, r1].some((x) => x === null) || a0 === 0 || b0 === 0) continue;
    const dA = ((a1 - a0) / a0) * 100;
    const dB = ((b1 - b0) / b0) * 100;
    decomp.push({
      from: header[k + 1] || `열 ${k + 1}`,
      to: header[k] || `열 ${k}`,
      dA, dB, dR: r1 - r0,
    });
  }
  const decompHtml = decomp.length
    ? decomp
        .map(
          (d) => `<div class="decomp">
            <div class="decomp-head">${d.from} → ${d.to}</div>
            <ul class="plain-list">
              <li>가용자본(분자) ${d.dA >= 0 ? "+" : ""}${d.dA.toFixed(1)}%</li>
              <li>요구자본(분모) ${d.dB >= 0 ? "+" : ""}${d.dB.toFixed(1)}%</li>
              <li>지급여력비율 ${d.dR >= 0 ? "+" : ""}${d.dR.toFixed(1)}%p</li>
            </ul>
            <p class="decomp-txt">${
              d.dB > d.dA
                ? "요구자본이 가용자본보다 빠르게 증가해 비율을 낮추는 방향으로 작용했습니다."
                : d.dA > d.dB
                ? "가용자본이 요구자본보다 빠르게 증가해 비율을 높이는 방향으로 작용했습니다."
                : "분자와 분모가 비슷한 속도로 변동했습니다."
            } 이는 공시된 두 숫자만으로 산술적으로 확인되는 사실이며, 그 변화가 왜 일어났는지(금리·주가·제도변경 등)는 이 데이터만으로 단정할 수 없습니다.</p>
          </div>`
        )
        .join("")
    : "";

  return `
    <div class="kics-cand">
      ${total > 1 ? `<div class="cand-badge">수치가 다른 표 ${idx + 1} / ${total}</div>` : ""}
      ${c.sourceTableCount > 1 ? `<div class="cand-note">이 보고서의 서로 다른 ${c.sourceTableCount}개 표에서 동일한 수치가 확인됐습니다.</div>` : ""}
      ${c.nearestHeading ? `<div class="cand-heading">보고서 내 소제목: ${c.nearestHeading}</div>` : ""}
      ${c.otherInsurersMentionedNearby && c.otherInsurersMentionedNearby.length
        ? `<div class="ifrs-boundary"><span class="boundary-label">주의 — 다른 보험사가 함께 언급된 표</span>
            이 표 주변에 ${c.otherInsurersMentionedNearby.join(", ")}이(가) 언급됩니다. 계열 보험사의 수치가 같은 보고서에 실린 것일 수 있으므로 DART 원문에서 확인하세요.</div>`
        : ""}
      <div class="table-scroll"><table class="fin-table">
        <thead><tr>${header.map((h, i) => `<th>${h}</th>`).join("")}</tr></thead>
        <tbody>
          ${rowHtml("가용자본", av)}
          ${rowHtml("요구자본", rq)}
          ${rowHtml("비율", rt)}
        </tbody>
      </table></div>
      <div class="unit-note">${renderUnitNote(c)}</div>

      <h5 class="sub-h">사이트 검산 — 공시값과 비교</h5>
      ${checkHtml}

      ${decompHtml ? `<h5 class="sub-h">비율 변화의 산술적 분해</h5>${decompHtml}` : ""}

      ${c.contextAfter ? `<details class="ctx"><summary>보고서 각주 원문 보기 (제도 전환·정정공시 여부 확인)</summary><p>${c.contextAfter}</p></details>` : ""}
    </div>
  `;
}

function renderKicsTheoryLinks() {
  const k = MAPPING.kics || {};
  const rows = Object.entries(k)
    .map(
      ([name, v]) => `<div class="field">
        <span class="label">${name}</span>
        <div class="theory-text">${v.what}</div>
        <div class="chips">${(v.kicsSections || [])
          .map((s) => {
            const ch = KICS.chapters.find((c) => c.num === s);
            return ch ? `<button class="chip clickable" data-kicsch="${s}">K-ICS 해설서 ${ch.num}. ${ch.title}</button>` : "";
          })
          .join("")}</div>
        <p class="panel-note small">${v.note}</p>
      </div>`
    )
    .join("");
  return `<div class="bridge-card"><h4>이 숫자들은 이론적으로 어떻게 만들어지는가</h4>${rows}</div>`;
}

async function loadSourcePanel() {
  const panel = document.getElementById("coPanel");
  const co = CURRENT_CO;
  const fin = CACHE.ifrs17[co.corpCode];
  const kics = CACHE.kics[co.corpCode];

  const finRows = fin && fin.years
    ? fin.years
        .map(
          (y) =>
            `<tr><td>${y.bsnsYear} 사업연도</td><td>사업보고서 (연간, reprt_code 11011)</td><td>${
              y.fsDiv === "CFS" ? "연결재무제표(CFS)" : "개별재무제표(OFS)"
            }</td><td>OpenDART fnlttSinglAcntAll</td></tr>`
        )
        .join("")
    : `<tr><td colspan="4" class="na">IFRS17 탭을 먼저 열면 조회 출처가 표시됩니다.</td></tr>`;

  const kicsRows = kics && kics.reports
    ? kics.reports
        .map(
          (r) =>
            `<tr><td>${r.reportName}</td><td>${r.rceptDt}</td><td>${r.rceptNo}</td>
             <td><a class="dart-link" href="${r.dartOriginalUrl}" target="_blank" rel="noopener">원문 열기</a></td></tr>`
        )
        .join("")
    : `<tr><td colspan="4" class="na">K-ICS 탭을 먼저 열면 조회 출처가 표시됩니다.</td></tr>`;

  panel.innerHTML = `
    <h4 class="sec-h">재무제표 숫자의 출처</h4>
    <div class="table-scroll"><table class="fin-table">
      <thead><tr><th>사업연도</th><th>보고서</th><th>재무제표 구분</th><th>API</th></tr></thead>
      <tbody>${finRows}</tbody>
    </table></div>

    <h4 class="sec-h">K-ICS 숫자의 출처 (사업보고서 원문)</h4>
    <div class="table-scroll"><table class="fin-table">
      <thead><tr><th>보고서명</th><th>접수일</th><th>접수번호</th><th>DART</th></tr></thead>
      <tbody>${kicsRows}</tbody>
    </table></div>

    <div class="bridge-card">
      <h4>데이터 취급 원칙</h4>
      <ul class="plain-list">
        <li>모든 숫자는 금융감독원 OpenDART에서 조회한 회사 공시값이며, 사이트가 가공하지 않습니다.</li>
        <li>값이 없는 경우를 0으로 처리하지 않고, '계정 확인 불가' · '공시에서 K-ICS 정보 확인 불가' · '해당 사업연도 사업보고서 없음' · 'DART 조회 중 오류 발생'을 서로 구분해 표시합니다.</li>
        <li>K-ICS는 전용 API가 없어 사업보고서 원문 표를 패턴으로 추출합니다. 후보 표가 여러 개면 자동으로 하나를 고르지 않고 모두 보여줍니다.</li>
        <li>RBC→K-ICS 제도 전환으로 연도 간 산출기준이 다를 수 있어, 표의 기준 표시와 각주를 함께 확인하도록 안내합니다.</li>
        <li>이 화면은 투자판단·회사 우열평가를 제공하지 않습니다.</li>
      </ul>
    </div>
  `;
}
