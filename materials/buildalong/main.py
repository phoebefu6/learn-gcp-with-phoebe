# Builder session 6: an ingest function, run locally with functions-framework (no Cloud Run needed).
# Needs: pip install functions-framework==3.10.2
# Run:   functions-framework --target=ingest --port=8080
import re
import functions_framework

HIVE = re.compile(r"^sales/dt=(\d{4}-\d{2}-\d{2})/[^/]+\.parquet$")

@functions_framework.http
def ingest(request):
    event = request.get_json(silent=True) or {}
    bucket, name = event.get("bucket", ""), event.get("name", "")
    m = HIVE.match(name)
    if not m:
        return {"status": "rejected", "reason": "path is not sales/dt=YYYY-MM-DD/*.parquet", "name": name}, 400
    return {"status": "accepted",
            "load": f"gs://{bucket}/{name}",
            "into": f"tw-lake-prod.sales_raw.orders${m.group(1).replace('-', '')}"}, 200
