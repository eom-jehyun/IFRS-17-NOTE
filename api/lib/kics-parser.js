// K-ICS 지급여력비율 표 추출기 (Node 포팅판).
// scripts_audit/kics_table_extractor_v2.py 에서 삼성생명·DB손해보험 실제 사업보고서 원문으로
// 검증한 로직을 그대로 옮긴 것. 파이썬 버전에서 발견한 오탐 사례 3가지를 반영한 필터가 들어있다:
//   1) '주요 경영지표' 표의 ROA/ROE 행이 가용자본/요구자본으로 잘못 잡히는 경우 → (A)/(B) 마커 필수화로 제거
//   2) 이사회 회의록 표의 안건명 '지급여력비율 ...' → 위와 동일 필터로 제거
//   3) 자회사(RBC 비율) 표가 같은 셀 패턴이라 섞이는 경우 → 표 앞 소제목에 'RBC' 있으면 제외
//
// 미해결로 남아있는 함정(코드 주석 그대로 유지): DB손해보험 사업보고서에는 계열사인
// DB생명보험의 K-ICS 표가 별도 섹션에 같이 실려 있었고, 그 사실은 표가 아니라 표 "뒤" 각주에서만
// 확인 가능했다. 이 v1 로직은 표 "앞" 컨텍스트만 보므로 이 케이스를 자동으로 걸러내지 못한다.
// 그래서 이 함수는 여러 후보가 남을 경우 절대 하나를 자동으로 고르지 않고 전부 반환하며,
// 호출부(UI)가 "이 회사 보고서에서 발견된 표가 N개입니다"라고 사용자에게 보여주고 판단하게 한다.

const TABLE_RE = /<TABLE\b[\s\S]*?<\/TABLE>/gi;
const TR_RE = /<TR\b[\s\S]*?<\/TR>/gi;
const CELL_RE = /<(TD|TH)\b[^>]*>([\s\S]*?)<\/\1>/gi;
const TAG_RE = /<[^>]+>/g;
const HEADING_RE = /<P[^>]*USERMARK="B"[^>]*>([\s\S]*?)<\/P>/gi;

// "타깃 회사명이 없다"는 신호는 신뢰할 수 없다 (사업보고서는 자기 회사를 '당사'/'연결실체'로 부르는
// 경우가 대부분이라 정상적인 표에도 회사명이 아예 안 나올 수 있음 — 실제 삼성생명 표에서 확인됨).
// 대신 "다른 보험사 이름이 나온다"는 신호만 의미가 있다 (DB손해보험 사업보고서 안에 계열사인
// DB생명보험 표가 섞여 있던 사례로 확인됨). 그래서 판단 기준을 curated insurer 목록 기반으로 바꾼다.
const { INSURERS } = require("./insurers.js");

function cellText(raw) {
  return raw.replace(TAG_RE, "").replace(/\s+/g, " ").trim();
}

function parseRow(trHtml) {
  const cells = [];
  let m;
  const re = new RegExp(CELL_RE.source, "gi");
  while ((m = re.exec(trHtml))) cells.push(cellText(m[2]));
  return cells;
}

function classifyCell(s) {
  const t = s.trim();
  if (t === "-" || t === "" || t === "N/A") return "empty";
  if (/^-?[\d,]+(\.\d+)?$/.test(t)) return "number";
  return "placeholder_text";
}

/**
 * @param {string} xmlText 사업보고서 원문 XML (document.xml API로 받은 zip 안의 파일)
 * @param {string} targetCorpName 대상 회사명 (다른 회사 언급 감지용)
 * @returns {object[]} 필터를 통과한 K-ICS 후보 표 목록
 */
function findKicsTables(xmlText, targetCorpName) {
  const results = [];
  let tblMatch;
  const tableRe = new RegExp(TABLE_RE.source, "gi");
  while ((tblMatch = tableRe.exec(xmlText))) {
    const tblHtml = tblMatch[0];
    if (!tblHtml.includes("지급여력비율")) continue;

    const trRe = new RegExp(TR_RE.source, "gi");
    let trMatch;
    const rows = [];
    while ((trMatch = trRe.exec(tblHtml))) {
      const row = parseRow(trMatch[0]);
      if (row.some((c) => c.trim())) rows.push(row);
    }

    const ratioIdx = rows.findIndex((r) => r[0] && r[0].startsWith("지급여력비율"));
    if (ratioIdx < 2) continue;

    const availRow = rows[ratioIdx - 2];
    const reqdRow = rows[ratioIdx - 1];
    const ratioRow = rows[ratioIdx];

    if (!/[\(（]\s*A\s*[\)）]/.test(availRow[0])) continue;
    if (!/[\(（]\s*B\s*[\)）]/.test(reqdRow[0])) continue;

    const headerRow = rows[0][0] !== availRow[0] ? rows[0] : null;

    const start = tblMatch.index;
    const window = xmlText.slice(Math.max(0, start - 3000), start);
    const headingRe = new RegExp(HEADING_RE.source, "gi");
    let headingMatch;
    let lastHeading = null;
    while ((headingMatch = headingRe.exec(window))) lastHeading = cellText(headingMatch[1]);
    if (lastHeading && lastHeading.includes("RBC")) continue;

    const contextRaw = xmlText.slice(Math.max(0, start - 900), start).replace(TAG_RE, " ");
    const contextPlain = contextRaw.replace(/\s+/g, " ").trim();
    const afterRaw = xmlText.slice(tblMatch.index + tblHtml.length, tblMatch.index + tblHtml.length + 900).replace(TAG_RE, " ");
    const afterPlain = afterRaw.replace(/\s+/g, " ").trim();
    const combinedContext = `${contextPlain} ${afterPlain}`;

    const otherInsurersMentioned = INSURERS
      .map((c) => c.name)
      .filter((name) => name !== targetCorpName && !name.startsWith(targetCorpName) && !targetCorpName.startsWith(name))
      .filter((name) => combinedContext.includes(name));

    results.push({
      nearestHeading: lastHeading,
      header: headerRow,
      availableCapitalRow: availRow,
      requiredCapitalRow: reqdRow,
      ratioRow: ratioRow,
      cellKinds: {
        avail: availRow.slice(1).map(classifyCell),
        reqd: reqdRow.slice(1).map(classifyCell),
        ratio: ratioRow.slice(1).map(classifyCell),
      },
      // 사용자가 직접 판단할 수 있도록 표 앞/뒤 문맥을 그대로 넘긴다 (자동 판별 대신 투명성 확보)
      contextBefore: contextPlain.slice(-400),
      contextAfter: afterPlain.slice(0, 400),
      otherInsurersMentionedNearby: otherInsurersMentioned,
    });
  }
  return results;
}

module.exports = { findKicsTables };
