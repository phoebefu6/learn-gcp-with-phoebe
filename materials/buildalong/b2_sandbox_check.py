# Builder session 2: check the sandbox query's LOGIC on the shipped sample with DuckDB.
# The numbers differ from BigQuery's full table: the sample is 18,362 trips, the table about 212 million.
# Needs: pip install duckdb==2.0.0
import sys, duckdb
SRC = sys.argv[1] if len(sys.argv) > 1 else "chicago_taxi_sample.parquet"
con = duckdb.connect()
con.execute(f"CREATE VIEW taxi_trips AS SELECT * FROM '{SRC}'")
sql = """
SELECT payment_type,
       COUNT(*)            AS trips,
       ROUND(AVG(fare), 2) AS avg_fare
FROM taxi_trips
WHERE trip_start_timestamp >= TIMESTAMP '2019-01-01'
  AND trip_start_timestamp <  TIMESTAMP '2020-01-01'
GROUP BY payment_type
ORDER BY trips DESC
"""
for row in con.execute(sql).fetchall():
    print(f"{row[0]:12s} {row[1]:>6d} {row[2]:>8.2f}")
