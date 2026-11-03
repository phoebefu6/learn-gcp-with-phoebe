// Runs assets/gcp-iam.js on the same fixture in node and prints the result as JSON (compare with iam_eval.py --json).
const path = require("path");
const I = require(path.join(__dirname, "..", "assets", "gcp-iam.js"));
const D = { fixture: require(path.join(__dirname, "iam-fixture.json")), roles: require(path.join(__dirname, "roles-2026-11-03.json")) };
console.log(JSON.stringify(I.make(D).run(), null, 1));
