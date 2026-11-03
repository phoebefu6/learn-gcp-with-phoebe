"""Write data/chicago_taxi_sample.parquet: the 18,362 seeded portal trips with BigQuery's column names
and types (STRING / INT64 / FLOAT64 / TIMESTAMP), so laptop build-alongs read the same rows the cost
bench measures. Run with the scratch venv (pyarrow 25.0.1): python make-parquet.py <fetch out dir>"""
import glob, json, os, sys, datetime as dt
import pyarrow as pa, pyarrow.parquet as pq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = __import__("importlib").import_module("build_sample_schema")
rows = [r for f in sorted(glob.glob(os.path.join(SRC, "slots", "*.json"))) for r in json.load(open(f))]
T = {"STRING": pa.string(), "INT64": pa.int64(), "FLOAT64": pa.float64(), "TIMESTAMP": pa.timestamp("us", tz="UTC")}
def conv(t, v):
    if v is None: return None
    if isinstance(v, dict):
        lon, lat = v["coordinates"]; return "POINT (%s %s)" % (repr(float(lon)), repr(float(lat)))
    if t == "INT64": return int(float(v))
    if t == "FLOAT64": return float(v)
    if t == "TIMESTAMP": return dt.datetime.fromisoformat(v).replace(tzinfo=dt.timezone.utc)
    return v
cols = {n: pa.array([conv(t, r.get(f)) for r in rows], type=T[t]) for n, t, f in spec.SCHEMA}
tbl = pa.table(cols).sort_by("trip_start_timestamp")
os.makedirs(os.path.join(REPO, "data"), exist_ok=True)
out = os.path.join(REPO, "data", "chicago_taxi_sample.parquet")
pq.write_table(tbl, out, compression="zstd")
print("rows", tbl.num_rows, "cols", tbl.num_columns, "bytes", os.path.getsize(out))
