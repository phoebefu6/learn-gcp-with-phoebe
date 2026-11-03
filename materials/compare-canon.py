"""Compare python and node canon BY VALUE (IAM verdicts + cost ladder). Exit 1 on any difference.
Self-test: --plant perturbs one node ladder byte count by 0.1% and must make the comparison fail."""
import json, subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__))
def sh(cmd): return json.loads(subprocess.check_output(cmd, cwd=H))
iam_py, iam_js = sh([sys.executable, "iam_eval.py", "--json"]), sh(["node", "run-iam-node.js"])
cost_py, cost_js = sh([sys.executable, "cost_ref.py", "--json"]), sh(["node", "run-cost-node.js"])
if "--plant" in sys.argv:
    cost_js[2]["bytes"] = int(cost_js[2]["bytes"] * 1.001)
bad = []
for a, b in zip(iam_py["cases"], iam_js["cases"]):
    if a != b: bad.append(("iam case", a, b))
if iam_py["scores"] != iam_js["scores"]: bad.append(("iam scores", iam_py["scores"], iam_js["scores"]))
if iam_py["antilever"] != iam_js["antilever"]: bad.append(("antilever", iam_py["antilever"], iam_js["antilever"]))
for a, b in zip(cost_py, cost_js):
    for k in ("id", "rows", "bytes", "billed"):
        if a[k] != b[k]: bad.append(("ladder " + a["id"], k, a[k], b[k]))
    if abs(a["cost"] - b["cost"]) > 1e-12: bad.append(("ladder cost", a["id"], a["cost"], b["cost"]))
    if (a["blocks"] or None) != (b["blocks"] or None): bad.append(("blocks", a["blocks"], b["blocks"]))
print("IAM", iam_py["scores"], iam_py["antilever"])
for r in cost_py: print("ladder", r["id"], r["rows"], r["bytes"], r["billed"], round(r["cost"], 6))
print("DIFFERENCES:", bad if bad else "none")
sys.exit(1 if bad else 0)
