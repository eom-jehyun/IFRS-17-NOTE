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
  // Vary: Origin 은 반드시 필요하다.
  // 응답이 요청 Origin에 따라 달라지는데 CDN이 이를 캐시 키에 넣지 않으면,
  // 제3자가 임의 Origin으로 먼저 호출해 'ACAO 헤더 없는 응답'을 캐시에 올려두면
  // 이후 우리 사이트(github.io)가 그 캐시본을 받아 브라우저에서 차단된다.
  // (프로덕션에서 실제로 재현 확인함: evil origin MISS → github.io HIT → ACAO 없음)
  res.setHeader("Vary", "Origin");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", `s-maxage=${sMaxAge}, stale-while-revalidate=600`);
}

module.exports = { applyCors };
