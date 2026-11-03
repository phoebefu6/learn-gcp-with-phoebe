# Builder session 5: an Apache Beam pipeline on the DirectRunner (your laptop), no Dataflow needed.
# Needs: pip install apache-beam==2.77.0
import sys
import apache_beam as beam
from apache_beam.transforms.window import FixedWindows, TimestampedValue
from apache_beam.options.pipeline_options import PipelineOptions

SRC = sys.argv[1] if len(sys.argv) > 1 else "chicago_taxi_sample.parquet"
opts = PipelineOptions(runner="DirectRunner")

with beam.Pipeline(options=opts) as p:
    trips = (p | "Read" >> beam.io.ReadFromParquet(SRC, columns=["trip_start_timestamp", "payment_type", "fare"])
               | "Has fare" >> beam.Filter(lambda r: r["fare"] is not None))
    (trips
     | "Key by year" >> beam.Map(lambda r: (r["trip_start_timestamp"].year, r["fare"]))
     | "Mean per year" >> beam.combiners.Mean.PerKey()
     | "Sort" >> beam.combiners.ToList()
     | "Print years" >> beam.Map(lambda rows: [print(f"year {y}  mean fare {m:6.2f}") for y, m in sorted(rows)]))
    (trips
     | "2019 only" >> beam.Filter(lambda r: r["trip_start_timestamp"].year == 2019)
     | "Event time" >> beam.Map(lambda r: TimestampedValue(r["payment_type"], r["trip_start_timestamp"].timestamp()))
     | "30-day windows" >> beam.WindowInto(FixedWindows(30 * 24 * 3600))
     | "Count in window" >> beam.combiners.Count.Globally().without_defaults()
     | "Collect" >> beam.WindowInto(beam.window.GlobalWindows())
     | "All windows" >> beam.combiners.ToList()
     | "Print windows" >> beam.Map(lambda ns: print("2019 trips per 30-day window:", sorted(ns, reverse=True))))
