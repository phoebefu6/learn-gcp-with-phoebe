# Builder session 4: ask the evaluator what Google's IAM rules say about five Tidewater requests.
# Same logic as the bench (iam_eval.py, the Python twin of the bench's gcp-iam.js).
import sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
import iam_eval as I
for cid in ["c05", "c06", "c08", "c09", "c12"]:
    c = next(x for x in I.FIX["cases"] if x["id"] == cid)
    q = c["request"]
    r = I.evaluate(q)
    where = r.get("at", "-")
    print(f"{cid} {q['principal'].split(':')[1]:52s} {q['permission']:28s} on {q['resource']:13s} -> {r['verdict']:11s} ({r['step']} at {where})")
    for line in r["trace"]:
        print("     trace:", line)
