const { applyCors } = require("./lib/cors.js");
const { fetchRecentYears } = require("./lib/dart.js");
const { extractIfrs17Accounts } = require("./lib/ifrs17-accounts.js");
const { INSURERS } = require("./lib/insurers.js");

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === "OPTIONS") return res.status(204).end();

  const corpCode = (req.query.corpCode || "").trim();
  const company = INSURERS.find((c) => c.corpCode === corpCode);
  if (!company) {
    return res.status(400).json({ error: "corpCode가 지원 대상 보험회사 목록에 없습니다." });
  }

  try {
    const yearlyResults = await fetchRecentYears(corpCode, 3);
    if (yearlyResults.length === 0) {
      return res.status(200).json({
        company,
        error: "해당 사업연도 사업보고서 없음",
        balanceSheet: [],
        incomeStatement: [],
      });
    }
    const data = extractIfrs17Accounts(yearlyResults);
    res.status(200).json({ company, ...data, source: "OpenDART fnlttSinglAcntAll" });
  } catch (err) {
    res.status(502).json({ error: "DART 조회 중 오류 발생", detail: String(err.message || err) });
  }
};
