const fs = require("fs");
const { findKicsTables } = require("../api/lib/kics-parser.js");

const [, , filePath, corpName] = process.argv;
const text = fs.readFileSync(filePath, "utf-8");
const tables = findKicsTables(text, corpName);

console.log(`파일: ${filePath} (타깃 회사: ${corpName})`);
console.log(`필터 통과 후보 표: ${tables.length}개\n`);
tables.forEach((t, i) => {
  const flag = t.otherInsurersMentionedNearby.length ? `⚠ 다른 보험사 언급: ${t.otherInsurersMentionedNearby.join(", ")}` : "";
  console.log(`--- 후보 ${i + 1} ${flag} ---`);
  console.log("  소제목:      ", t.nearestHeading);
  console.log("  헤더:        ", t.header);
  console.log("  가용자본 행:  ", t.availableCapitalRow, t.cellKinds.avail);
  console.log("  요구자본 행:  ", t.requiredCapitalRow, t.cellKinds.reqd);
  console.log("  비율 행:      ", t.ratioRow, t.cellKinds.ratio);
  console.log("  뒤 문맥:      ", t.contextAfter.slice(0, 150));
  console.log();
});
