// DART OpenAPI 공통 helper. 기존 dart-financial-search/src/lib/dart.ts 의 로직(연결→개별 fallback,
// 최근 사업연도 자동탐지)을 이 프로젝트 전용 Vercel 서버리스 함수용으로 옮긴 것.
// DART_API_KEY는 Vercel 프로젝트 환경변수로만 존재하며 이 파일 밖으로 나가지 않는다.

const FNLTT_URL = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json";
const DOCUMENT_URL = "https://opendart.fss.or.kr/api/document.xml";
const LIST_URL = "https://opendart.fss.or.kr/api/list.json";
const REPRT_CODE_ANNUAL = "11011"; // 사업보고서(연간)

function apiKey() {
  const key = process.env.DART_API_KEY;
  if (!key) throw new Error("DART_API_KEY 환경변수가 설정되지 않았습니다.");
  return key;
}

/** 당해 사업보고서는 통상 다음해 3월에 공시되므로, 3월 이전에는 전전년도부터 시도한다. */
function candidateYears(count = 3) {
  const now = new Date();
  const startYear = now.getMonth() + 1 >= 4 ? now.getFullYear() - 1 : now.getFullYear() - 2;
  const years = [];
  for (let i = 0; i < count + 1; i++) years.push(startYear - i);
  return years;
}

async function fetchAccountsOneYear(corpCode, bsnsYear, fsDiv) {
  const params = new URLSearchParams({
    crtfc_key: apiKey(),
    corp_code: corpCode,
    bsns_year: String(bsnsYear),
    reprt_code: REPRT_CODE_ANNUAL,
    fs_div: fsDiv,
  });
  const res = await fetch(`${FNLTT_URL}?${params.toString()}`);
  if (!res.ok) return null;
  const data = await res.json();
  if (data.status !== "000" || !Array.isArray(data.list) || data.list.length === 0) {
    return null;
  }
  return data.list;
}

/**
 * 최근 N개 사업연도의 재무제표를 연결(CFS) 우선, 실패 시 개별(OFS)로 대체하여 가져온다.
 * 각 연도는 독립적으로 CFS/OFS를 시도한다 (연도별로 연결/개별이 섞일 수 있음을 호출부에 알려준다).
 */
async function fetchRecentYears(corpCode, yearsCount = 3) {
  const years = candidateYears(yearsCount + 1); // 여유분 포함해서 시도
  const results = [];
  for (const year of years) {
    if (results.length >= yearsCount) break;
    for (const fsDiv of ["CFS", "OFS"]) {
      const items = await fetchAccountsOneYear(corpCode, year, fsDiv);
      if (items) {
        results.push({ bsnsYear: year, fsDiv, items });
        break;
      }
    }
  }
  return results; // 최신순
}

async function fetchDisclosureList(corpCode, { bgnDe, endDe, pblntfTy = "A" } = {}) {
  const params = new URLSearchParams({
    crtfc_key: apiKey(),
    corp_code: corpCode,
    bgn_de: bgnDe,
    end_de: endDe,
    pblntf_ty: pblntfTy,
    page_count: "100",
  });
  const res = await fetch(`${LIST_URL}?${params.toString()}`);
  if (!res.ok) return [];
  const data = await res.json();
  if (data.status !== "000" || !Array.isArray(data.list)) return [];
  return data.list;
}

/**
 * 특정 rcept_no(접수번호)의 사업보고서 원문 zip을 받아온다. 호출부에서 압축을 푼다.
 *
 * 주의: DART는 원문이 없을 때도 HTTP 200으로 응답하고 본문에 XML 오류를 담아 보낸다.
 * 실제 확인된 예: 삼성화재 [첨부정정]사업보고서(20260313001226) → status 014 "파일이 존재하지 않습니다".
 * 그래서 zip 매직바이트(PK)를 직접 검사하고, zip이 아니면 DART가 준 메시지를 그대로 올려보낸다.
 */
async function fetchDocumentZip(rceptNo) {
  const params = new URLSearchParams({ crtfc_key: apiKey(), rcept_no: rceptNo });
  const res = await fetch(`${DOCUMENT_URL}?${params.toString()}`);
  if (!res.ok) throw new Error(`DART document API 오류: HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());

  if (buf.length < 4 || buf[0] !== 0x50 || buf[1] !== 0x4b) {
    const text = buf.toString("utf-8").slice(0, 500);
    const status = (text.match(/<status>([^<]*)<\/status>/) || [])[1];
    const message = (text.match(/<message>([^<]*)<\/message>/) || [])[1];
    const err = new Error(
      message ? `DART 원문 미제공 (status ${status}: ${message})` : "DART 원문이 zip 형식이 아닙니다."
    );
    err.dartStatus = status || null;
    err.dartMessage = message || null;
    throw err;
  }
  return buf;
}

module.exports = {
  candidateYears,
  fetchAccountsOneYear,
  fetchRecentYears,
  fetchDisclosureList,
  fetchDocumentZip,
};
