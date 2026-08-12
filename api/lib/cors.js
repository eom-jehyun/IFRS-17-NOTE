// PHASE 12: GitHub Pages(정적 프론트) origin만 명시적으로 허용한다.
// 로컬 개발 시에는 localhost도 허용하되, 운영 응답에는 아무 사이트나 이 API를 가져다 쓸 수 없게 한다.
const ALLOWED_ORIGINS = [
  "https://eom-jehyun.github.io",
  "http://localhost:3000",
  "http://127.0.0.1:3000",
];

/**
 * @param {number} sMaxAge CDN 캐시 유지시간(초). 공시데이터는 자주 바뀌지 않으므로
 *   엔드포인트별로 다르게 준다. 사업보고서 원문을 파싱하는 K-ICS는 더 길게 캐시해
 *   반복 방문 시 DART를 다시 호출하지 않도록 한다.
 */
function applyCors(req, res, sMaxAge = 3600) {
  const origin = req.headers.origin;
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
  }
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", `s-maxage=${sMaxAge}, stale-while-revalidate=600`);
}

module.exports = { applyCors };
