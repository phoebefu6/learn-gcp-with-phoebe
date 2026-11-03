# Builder session 1: lay out a lake the way Cloud Storage + BigQuery expect it, on a laptop.
# Needs: pip install pyarrow==25.0.1   Data: chicago_taxi_sample.parquet (18,362 real trips)
import os, sys, glob, shutil
import pyarrow.parquet as pq, pyarrow.csv as pacsv, pyarrow.compute as pc, pyarrow.dataset as ds

SRC = sys.argv[1] if len(sys.argv) > 1 else "chicago_taxi_sample.parquet"
LAKE = "tw-lake"                      # stands in for gs://tw-lake-prod-landing
shutil.rmtree(LAKE, ignore_errors=True)
t = pq.read_table(SRC)
print("rows", t.num_rows, "columns", t.num_columns)

# 1. the same rows, two formats
os.makedirs(f"{LAKE}/flat", exist_ok=True)
pacsv.write_csv(t, f"{LAKE}/flat/trips.csv")
pq.write_table(t, f"{LAKE}/flat/trips.parquet", compression="snappy")
for f in sorted(glob.glob(f"{LAKE}/flat/*")):
    print(f"{f:32s} {os.path.getsize(f):>12,d} bytes")

# 2. hive-style partitions: key=value folders that BigQuery external tables can read
t = t.append_column("year", pc.year(t["trip_start_timestamp"]))
pq.write_to_dataset(t, f"{LAKE}/sales_raw/taxi", partition_cols=["year"],
                    basename_template="part-{i}.parquet")
parts = sorted(glob.glob(f"{LAKE}/sales_raw/taxi/year=*/*.parquet"))
print("partition files", len(parts), "first", parts[0], "last", parts[-1])

# 3. a filter on the partition key opens only the matching folder
d = ds.dataset(f"{LAKE}/sales_raw/taxi", format="parquet", partitioning="hive")
frags = list(d.get_fragments(filter=ds.field("year") == 2019))
print("files read for year = 2019:", len(frags), "of", len(parts))
print("rows in 2019:", d.to_table(filter=ds.field("year") == 2019).num_rows)
