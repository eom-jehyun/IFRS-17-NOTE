// 실제 DART fnlttSinglAcntAll 응답에서 확인된 결과(2024 사업연도, 삼성생명/DB손해보험 CFS)를 근거로
// 만든 IFRS17 관련 계정 분류기.
//
// 확인된 사실:
//  - 재무상태표 계정명(보험계약자산/부채, 재보험계약자산/부채)은 두 회사가 동일하게 사용함 → 안전하게 exact 매칭 가능.
//  - 손익계산서 계정명은 회사마다 다름
//      · 삼성생명: 보험손익 / 보험서비스수익·비용 / 출재보험서비스수익·비용 / 일반보험서비스수익·비용 /
//                 보험금융수익·비용 / 재보험금융수익·비용
//      · DB손해보험: 보험손익 / 보험수익 / 보험영업수익 / 재보험수익 / 보험비용 / 재보험비용 / 보험서비스비용 /
//                   보험금융수익·비용 / 보험계약자산(부채)순금융손익
//    → 손익계산서는 고정된 계정 목록으로 강제하지 않고, "보험" 키워드가 들어간 손익계산서 항목을 모두
//      원래 계정명 그대로 보여준다 (PHASE 14가 명시한 "위 계정이 반드시 존재한다고 가정하지 않는다"는
//      원칙을 지키기 위함). 재무상태표 4개 항목만 고정 카테고리로 분류한다.

const BS_CATEGORIES = [
  { key: "insuranceContractAssets", label: "보험계약자산", match: (n) => n === "보험계약자산" },
  { key: "reinsuranceContractAssets", label: "재보험계약자산", match: (n) => n === "재보험계약자산" },
  { key: "insuranceContractLiabilities", label: "보험계약부채", match: (n) => n === "보험계약부채" },
  { key: "reinsuranceContractLiabilities", label: "재보험계약부채", match: (n) => n === "재보험계약부채" },
];

// 손익계산서(IS/CIS)에서 "보험" 이 들어간 계정은 전부 채택하되, 재무상태표 계정과 중복되지 않게 제외.
function isIncomeStatementInsuranceAccount(item) {
  if (!["IS", "CIS"].includes(item.sj_div)) return false;
  if (!item.account_nm || !item.account_nm.includes("보험")) return false;
  return true;
}

// 일부 회사(예: 삼성생명)는 IFRS17 계정과 함께 과거 IFRS4 기준 비교계정을
// '보험료수익_IFRS4', '보험계약부채전입액_IFRS4' 처럼 함께 공시한다.
// 이를 IFRS17 계정으로 섞어 보여주면 오해를 유발하므로 별도로 표시(legacy)한다.
function isLegacyIfrs4(accountName) {
  return /IFRS\s*4/i.test(accountName);
}

function toNumber(s) {
  if (s === undefined || s === null) return null;
  const t = String(s).trim();
  if (t === "" || t === "-") return null;
  const n = Number(t.replace(/,/g, ""));
  return Number.isFinite(n) ? n : null;
}

/**
 * @param {{bsnsYear:number, fsDiv:string, items:any[]}[]} yearlyResults 최신순(내림차순) 연도별 원본 계정 목록
 * @returns {{ balanceSheet: object[], incomeStatement: object[], meta: object }}
 */
function extractIfrs17Accounts(yearlyResults) {
  const years = yearlyResults.map((y) => ({ bsnsYear: y.bsnsYear, fsDiv: y.fsDiv }));

  const balanceSheet = BS_CATEGORIES.map((cat) => {
    const byYear = yearlyResults.map((y) => {
      const found = y.items.find((it) => it.sj_div === "BS" && cat.match(it.account_nm));
      return {
        bsnsYear: y.bsnsYear,
        fsDiv: y.fsDiv,
        rawAccountName: found ? found.account_nm : null,
        amount: found ? toNumber(found.thstrm_amount) : null,
        status: found ? "found" : "계정 확인 불가",
      };
    });
    return { key: cat.key, label: cat.label, values: attachDiffs(byYear) };
  });

  // 손익계산서: 계정명 기준으로 그룹핑 (연도마다 계정명이 완전히 같다는 보장이 없으므로 계정명을 key로 묶는다)
  const nameSet = new Set();
  for (const y of yearlyResults) {
    for (const it of y.items) {
      if (isIncomeStatementInsuranceAccount(it)) nameSet.add(it.account_nm);
    }
  }
  const incomeStatement = Array.from(nameSet).map((name) => {
    const byYear = yearlyResults.map((y) => {
      const found = y.items.find((it) => isIncomeStatementInsuranceAccount(it) && it.account_nm === name);
      return {
        bsnsYear: y.bsnsYear,
        fsDiv: y.fsDiv,
        amount: found ? toNumber(found.thstrm_amount) : null,
        status: found ? "found" : "해당 연도 미공시 또는 계정 확인 불가",
      };
    });
    return { accountName: name, legacyIfrs4: isLegacyIfrs4(name), values: attachDiffs(byYear) };
  });

  return {
    years,
    balanceSheet,
    incomeStatement,
    note:
      "재무상태표 4개 항목(보험계약자산/부채, 재보험계약자산/부채)은 회사 간 동일한 계정명을 사용함을 " +
      "삼성생명·DB손해보험·삼성화재·현대해상 실제 공시로 확인했다. 손익계산서 항목은 회사마다, 심지어 " +
      "같은 회사의 연도별로도 계정명이 달라(예: 삼성생명 2023·2025년 '보험서비스결과' vs 2024년 미사용) " +
      "고정 목록 없이 공시된 원래 계정명을 그대로 노출한다. " +
      "'_IFRS4'가 붙은 계정은 과거 기준 비교계정이므로 legacyIfrs4=true로 구분한다.",
  };
}

function attachDiffs(byYearDesc) {
  // byYearDesc: 최신순 정렬. 증감은 (당해 - 전해)로 계산.
  return byYearDesc.map((cur, i) => {
    const prev = byYearDesc[i + 1];
    let diff = null;
    let pct = null;
    if (cur.amount !== null && prev && prev.amount !== null) {
      diff = cur.amount - prev.amount;
      if (prev.amount !== 0) pct = (diff / Math.abs(prev.amount)) * 100;
    }
    return { ...cur, diffFromPrevYear: diff, pctChangeFromPrevYear: pct };
  });
}

module.exports = { extractIfrs17Accounts };
