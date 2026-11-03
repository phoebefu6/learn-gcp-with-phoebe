"""Python reference for assets/gcp-cost.js: reproduces every cost-ladder byte count exactly.

Rules (read at source 2026-11-03):
- data type sizes: INT64 / FLOAT64 / TIMESTAMP 8 logical bytes, STRING 2 + UTF-8 size, NULL 0
  (https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types#data_type_sizes)
- "Charges are rounded up to the nearest MB, with a minimum 10 MB data processed per table referenced
  by the query, and with a minimum 10 MB data processed per query." (cloud.google.com/bigquery/pricing)
  MB is taken as 2^20 bytes (BigQuery's GiB and TiB are binary: "1 GiB is 2^30 bytes").
- on-demand $6.25 per TiB, first 1 TiB per month free (us-central1 default table, 2026-11-03).
Clustering is MODELLED: each January 2019 day partition sorted by pickup_community_area (NULLs
first) into fixed blocks of 5,000 rows; a filter reads every block its value touches.

Run: python cost_ref.py [--json]
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "gcp-sample.json")))
MB, TIB, BLOCK = 1 << 20, 1 << 40, 5000
NAMED = ["trip_start_timestamp", "pickup_community_area", "fare"]


def col_total(name):
    c = next(c for c in S["columns"] if c["name"] == name)
    return sum(k * v for k, v in c["hist"])


def scaled(cols, rows):
    a = sum(col_total(c) for c in cols)
    n = S["sample_rows"]
    return (2 * rows * a + n) // (2 * n)


def cluster_rows(value):
    total = blocks = allb = 0
    for d in S["jan2019"]["days"]:
        day_rows = sum(n for _, n in d["areas"])
        allb += math.ceil(day_rows / BLOCK)
        start = 0
        for v, n in d["areas"]:
            if v == value and n > 0:
                for b in range(start // BLOCK, (start + n - 1) // BLOCK + 1):
                    total += min(BLOCK, day_rows - b * BLOCK)
                    blocks += 1
            start += n
    return {"rows": total, "blocks": blocks, "allBlocks": allb}


def billed(b):
    return max(math.ceil(b / MB), 10) * MB


def run(cols, partition, cluster):
    blk = None
    if partition == "jan2019":
        if cluster is not None:
            blk = cluster_rows(cluster)
            rows = blk["rows"]
        else:
            rows = S["jan2019"]["rows"]
    else:
        rows = S["full_rows"]
    by = scaled(cols, rows)
    bb = billed(by)
    return {"rows": rows, "bytes": by, "billed": bb, "cost": bb / TIB * S["prices"]["on_demand_per_tib"], "blocks": blk}


def ladder():
    allc = [c["name"] for c in S["columns"]]
    spec = [("star", allc, "none", None), ("named", NAMED, "none", None),
            ("part", NAMED, "jan2019", None), ("clus", NAMED, "jan2019", 56)]
    out = []
    for i, c, p, k in spec:
        r = run(c, p, k)
        r["id"] = i
        out.append(r)
    return out


if __name__ == "__main__":
    L = ladder()
    if "--json" in sys.argv:
        print(json.dumps(L, indent=1, sort_keys=True))
    else:
        print("scale factor", S["full_rows"], "/", S["sample_rows"], "=", round(S["full_rows"] / S["sample_rows"], 1))
        for r in L:
            print("%-6s rows %12d bytes %15d (%.2f GiB) billed %15d cost $%.4f %s" % (
                r["id"], r["rows"], r["bytes"], r["bytes"] / (1 << 30), r["billed"], r["cost"],
                "" if not r["blocks"] else "blocks %d of %d" % (r["blocks"]["blocks"], r["blocks"]["allBlocks"])))
