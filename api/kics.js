const AdmZip = require("adm-zip");
const { applyCors } = require("./lib/cors.js");
const { fetchDisclosureList, fetchDocumentZip } = require("./lib/dart.js");
const { findKicsTables } = require("./lib/kics-parser.js");
const { INSURERS } = require("./lib/insurers.js");

function recentAnnualReports(disclosures, count = 3) {
  return disclosures
    .filter((d) => d.report_nm && d.report_nm.includes("사업보고서") && !d.report_nm.includes("분기") && !d.report_nm.includes("반기"))
    .sort((a, b) => (a.rcept_dt < b.rcept_dt ? 1 : -1))
    .slice(0, count);
}

// 동일 수치를 담은 표가 한 보고서 안에서 여러 번(예: 라벨만 '위험기준 지급여력기준(B)' /
// '지급여력기준(B)' 로 다른 절에 중복 게재) 발견되는 사례가 실제로 있었다.
// 수치가 완전히 같은 후보는 하나로 합치되, 몇 개의 표에서 나왔는지(sourceTableCount)를 남겨
// '자동으로 하나를 골랐다'는 오해가 없게 한다. 수치가 다르면 절대 합치지 않는다.
function dedupeCandidates(cands) {
  const out = [];
  for (const c of cands) {
    const key = JSON.stringify([
      (c.availableCapitalRow || []).slice(1),
      (c.requiredCapitalRow || []).slice(1),
      (c.ratioRow || []).slice(1),
      c.header,
    ]);
    const prev = out.find((o) => o._key === key);
    if (prev) {
      prev.sourceTableCount += 1;
      if (!prev.nearestHeading && c.nearestHeading) prev.nearestHeading = c.nearestHeading;
      continue;
    }
    out.push({ ...c, _key: key, sourceTableCount: 1 });
  }
  return out.map(({ _key, ...rest }) => rest);
}

module.exports = async (req, res) => {
  // 사업보고서 원문은 연 단위로 갱신되므로 CDN 캐시를 길게(12시간) 준다.
  applyCors(req, res, 43200);
  if (req.method === "OPTIONS") return res.status(204).end();

  const corpCode = (req.query.corpCode || "").trim();
  const company = INSURERS.find((c) => c.corpCode === corpCode);
  if (!company) {
    return res.status(400).json({ error: "corpCode가 지원 대상 보험회사 목록에 없습니다." });
  }

  try {
    const now = new Date();
    const bgnDe = `${now.getFullYear() - 3}0101`;
    const endDe = `${now.getFullYear()}1231`;
    const disclosures = await fetchDisclosureList(corpCode, { bgnDe, endDe });
    const annualReports = recentAnnualReports(disclosures, 3);

    if (annualReports.length === 0) {
      return res.status(200).json({
        company,
        error: "해당 사업연도 사업보고서 없음",
        reports: [],
      });
    }

    // 보고서 3건을 순차가 아니라 병렬로 내려받아 체감 지연을 줄인다(정확성에는 영향 없음).
    // 한 보고서의 원문이 없더라도(예: [첨부정정] 보고서는 DART가 원문을 제공하지 않음)
    // 나머지 보고서 결과는 정상적으로 보여주기 위해 보고서 단위로 오류를 격리한다.
    const reports = await Promise.all(
      annualReports.map(async (report) => {
        const base = {
          reportName: report.report_nm,
          rceptNo: report.rcept_no,
          rceptDt: report.rcept_dt,
          dartOriginalUrl: `https://dart.fss.or.kr/dsaf001/main.do?rcpNo=${report.rcept_no}`,
        };
        let zipBuf;
        try {
          zipBuf = await fetchDocumentZip(report.rcept_no);
        } catch (e) {
          return {
            ...base,
            kicsCandidates: [],
            note: `이 보고서는 DART가 원문 파일을 제공하지 않아 자동 추출할 수 없습니다. (${e.message}) 위 DART 원문 링크에서 직접 확인하세요.`,
            unavailable: true,
          };
        }
        const zip = new AdmZip(zipBuf);
        const entries = zip.getEntries().filter((e) => e.entryName.toLowerCase().endsWith(".xml"));

        let candidates = [];
        for (const entry of entries) {
          const xmlText = entry.getData().toString("utf-8");
          const found = findKicsTables(xmlText, company.name);
          candidates = candidates.concat(found.map((c) => ({ ...c, sourceFile: entry.entryName })));
        }
        candidates = dedupeCandidates(candidates);

        return {
          ...base,
          kicsCandidates: candidates,
          note:
            candidates.length === 0
              ? "공시에서 K-ICS 정보 확인 불가"
              : candidates.length > 1
                ? "이 보고서 안에서 수치가 서로 다른 지급여력비율 표가 여러 개 발견됐습니다. 자동으로 하나를 " +
                  "고르지 않았으니 각 후보의 소제목·각주를 보고 회사 자체의 표인지 확인하세요(계열 보험사 표가 " +
                  "함께 실리거나, 정정공시의 정정 전·후가 같이 담기는 경우가 있습니다)."
                : "표 1개 발견. 회사별 보고서 서식이 다양해 자동 추출한 결과이므로 DART 원문으로 대조 확인을 권장합니다.",
        };
      })
    );

    res.status(200).json({
      company,
      reports,
      source: "OpenDART document.xml (사업보고서 원문)",
      methodologyNote:
        "K-ICS 지급여력비율/가용자본/요구자본은 OpenDART에 전용 JSON API가 없어 사업보고서 원문 표를 " +
        "패턴 매칭으로 추출한다. 표의 '지급여력비율' 행을 찾고 그 위 2개 행을 가용자본/요구자본으로 " +
        "간주하며, (A)/(B) 마커가 없는 표(경영지표 요약, 이사회 회의록 등)는 제외한다. " +
        "RBC→K-ICS 제도 전환(2022~2023년경)으로 연도 간 산출방식이 다를 수 있으니 표에 표시된 " +
        "'(RBC 기준)'/'(K-ICS 기준)' 라벨을 반드시 함께 확인해야 한다.",
    });
  } catch (err) {
    res.status(502).json({ error: "DART 조회 중 오류 발생", detail: String(err.message || err) });
  }
};
