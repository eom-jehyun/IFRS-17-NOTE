const { applyCors } = require("./lib/cors.js");
const { INSURERS } = require("./lib/insurers.js");

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === "OPTIONS") return res.status(204).end();

  const q = (req.query.q || "").trim();
  const list = q
    ? INSURERS.filter((c) => c.name.includes(q))
    : INSURERS;

  res.status(200).json({
    query: q,
    count: list.length,
    companies: list,
    note:
      "이 프로젝트는 DART 범용 검색이 아니라 상장 보험회사로 범위를 제한한다. " +
      "교보생명·신한라이프·NH농협생명 등 비상장 보험사는 이 목록에 없다.",
  });
};
