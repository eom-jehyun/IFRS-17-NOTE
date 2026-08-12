// 로컬 통합 테스트용 서버. 정적파일 + /api/* 를 함께 서빙해 Vercel 배포 전에 end-to-end 확인한다.
// (배포에는 사용되지 않는다. Vercel은 api/ 폴더를 자동으로 서버리스 함수로 인식한다.)
//
// 사용법:  DART_API_KEY=... node scripts_audit/dev_server.js
const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");

const ROOT = path.join(__dirname, "..");
const PORT = 3000;

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".jpg": "image/jpeg",
  ".png": "image/png",
};

const handlers = {
  "/api/companies": require("../api/companies.js"),
  "/api/ifrs17": require("../api/ifrs17.js"),
  "/api/kics": require("../api/kics.js"),
};

const server = http.createServer(async (req, res) => {
  const parsed = url.parse(req.url, true);
  const pathname = parsed.pathname;

  if (handlers[pathname]) {
    // Vercel의 (req,res) 시그니처를 흉내내기 위해 query와 status/json을 붙여준다.
    req.query = parsed.query;
    res.status = (code) => {
      res.statusCode = code;
      return res;
    };
    res.json = (obj) => {
      res.setHeader("Content-Type", "application/json; charset=utf-8");
      res.end(JSON.stringify(obj));
    };
    try {
      await handlers[pathname](req, res);
    } catch (e) {
      res.statusCode = 500;
      res.end(JSON.stringify({ error: String(e.message || e) }));
    }
    return;
  }

  let filePath = path.join(ROOT, pathname === "/" ? "index.html" : decodeURIComponent(pathname));
  if (!filePath.startsWith(ROOT)) {
    res.statusCode = 403;
    res.end("forbidden");
    return;
  }
  fs.readFile(filePath, (err, buf) => {
    if (err) {
      res.statusCode = 404;
      res.end("not found");
      return;
    }
    res.setHeader("Content-Type", MIME[path.extname(filePath)] || "application/octet-stream");
    res.end(buf);
  });
});

server.listen(PORT, () => console.log(`dev server on http://localhost:${PORT}`));
