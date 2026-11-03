// Runs assets/gcp-cost.js on materials/gcp-sample.json in node and prints the ladder as JSON.
const path = require("path");
const C = require(path.join(__dirname, "..", "assets", "gcp-cost.js"));
const S = require(path.join(__dirname, "gcp-sample.json"));
const L = C.ladder(S).map(r => ({ id: r.id, rows: r.rows, bytes: r.bytes, billed: r.billed, cost: r.cost, blocks: r.blocks }));
console.log(JSON.stringify(L, null, 1));
