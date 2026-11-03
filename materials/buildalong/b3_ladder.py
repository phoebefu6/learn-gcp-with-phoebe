# Builder session 3: the bytes ladder, computed from BigQuery's documented data type sizes.
# Same engine as the bench (cost_ref.py, the Python twin of the bench's gcp-cost.js).
import os, sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
import cost_ref as C
GiB = 1 << 30
print(f"scale: {C.S['full_rows']:,} table rows / {C.S['sample_rows']:,} sample rows")
for r in C.ladder():
    extra = ""
    if r["blocks"]:
        extra = f"  ({r['blocks']['blocks']} of {r['blocks']['allBlocks']} modelled blocks)"
    print(f"{r['id']:6s} rows {r['rows']:>12,d}  processed {r['bytes'] / GiB:>9.4f} GiB  "
          f"billed {r['billed'] / (1 << 20):>10,.0f} MB  ${r['cost']:.4f}{extra}")
