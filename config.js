// ─────────────────────────────────────────────────────────────────────────────
// 배포 설정 — DART 백엔드 주소는 이 파일 한 곳에서만 관리한다.
//
// 구조:  GitHub Pages (정적 프론트)  →  Vercel 서버리스 함수  →  OpenDART
// DART API Key는 Vercel 환경변수(DART_API_KEY)에만 존재하며, 이 파일과 브라우저에는 없다.
//
// Vercel 배포 주소가 바뀌면 아래 VERCEL_API_BASE 한 줄만 수정하면 된다.
// (다른 파일에는 백엔드 주소를 중복해서 넣지 않는다.)
// ─────────────────────────────────────────────────────────────────────────────

const SITE_CONFIG = {
  // Vercel Production 주소 + "/api"
  VERCEL_API_BASE: "https://ifrs-17-note.vercel.app/api",

  // 로컬 개발 시 사용할 주소 (scripts_audit/dev_server.js)
  LOCAL_API_BASE: "http://localhost:3000/api",
};

/** 현재 접속 환경에 맞는 백엔드 주소를 돌려준다. */
SITE_CONFIG.apiBase = function () {
  const h = location.hostname;
  if (h === "localhost" || h === "127.0.0.1") return SITE_CONFIG.LOCAL_API_BASE;
  return SITE_CONFIG.VERCEL_API_BASE;
};
