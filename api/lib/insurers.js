// 이 프로젝트의 "보험사 분석" 모드는 DART 범용 검색이 아니라 보험회사로 범위를 제한한다 (PHASE 7).
// corp_code / stock_code 는 dart-financial-search/src/data/corp_codes.json (DART corpCode.xml에서
// 종목코드가 있는 상장기업만 추출한 로컬 데이터, 2025-07 기준)에서 확인된 값이다.
//
// 주의: 이 목록은 "상장" 보험사만 포함한다. 교보생명·신한라이프·NH농협생명·흥국생명 등
// 주요 비상장 보험사는 corp_codes.json이 상장기업만 필터링해서 만들어졌기 때문에 빠져 있다.
// 필요하면 DART corpCode.xml 전체(비상장 포함)에서 이들의 corp_code를 별도로 찾아 추가해야 한다.

const INSURERS = [
  { corpCode: "00126256", stockCode: "032830", name: "삼성생명", type: "life" },
  { corpCode: "00113058", stockCode: "088350", name: "한화생명", type: "life" },
  { corpCode: "00117267", stockCode: "082640", name: "동양생명", type: "life" },
  { corpCode: "00112332", stockCode: "085620", name: "미래에셋생명", type: "life" },
  { corpCode: "00139214", stockCode: "000810", name: "삼성화재해상보험", type: "nonlife" },
  { corpCode: "00159102", stockCode: "005830", name: "DB손해보험", type: "nonlife" },
  { corpCode: "00164973", stockCode: "001450", name: "현대해상화재보험", type: "nonlife" },
  { corpCode: "00120216", stockCode: "002550", name: "KB손해보험", type: "nonlife" },
  { corpCode: "00117744", stockCode: "000060", name: "메리츠화재해상보험", type: "nonlife" },
  { corpCode: "00135917", stockCode: "000370", name: "한화손해보험", type: "nonlife" },
  { corpCode: "00113562", stockCode: "000400", name: "롯데손해보험", type: "nonlife" },
  { corpCode: "00103176", stockCode: "000540", name: "흥국화재", type: "nonlife" },
];

module.exports = { INSURERS };
