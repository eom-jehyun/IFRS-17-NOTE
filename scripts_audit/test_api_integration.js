process.env.DART_API_KEY = require("fs").readFileSync(process.argv[2], "utf-8").split("\n")[1].trim();

const ifrs17Handler = require("../api/ifrs17.js");
const kicsHandler = require("../api/kics.js");

function mockReqRes(query) {
  const req = { method: "GET", query, headers: {} };
  const res = {
    _status: 200,
    status(code) { this._status = code; return this; },
    json(obj) {
      console.log(`[status ${this._status}]`);
      console.log(JSON.stringify(obj, null, 2).slice(0, 6000));
    },
    end() {},
    setHeader() {},
  };
  return { req, res };
}

async function main() {
  const corpCode = process.argv[3] || "00159102"; // DB손해보험

  console.log("========== /api/ifrs17 ==========");
  const a = mockReqRes({ corpCode });
  await ifrs17Handler(a.req, a.res);

  console.log("\n========== /api/kics ==========");
  const b = mockReqRes({ corpCode });
  await kicsHandler(b.req, b.res);
}

main().catch((e) => {
  console.error("FAILED:", e);
  process.exit(1);
});
