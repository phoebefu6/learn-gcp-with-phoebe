# Builder session 7: the model BigQuery ML would train, fitted on a laptop with numpy least squares.
# This is NOT BigQuery ML; it is the same idea (linear regression on fare) so you can read the SQL.
# Needs: pip install pyarrow==25.0.1 numpy (numpy 2.4.6 here)
import sys
import numpy as np, pyarrow.parquet as pq
SRC = sys.argv[1] if len(sys.argv) > 1 else "chicago_taxi_sample.parquet"
t = pq.read_table(SRC, columns=["trip_miles", "trip_seconds", "fare"]).to_pandas().dropna()
t = t[(t.trip_miles > 0) & (t.trip_miles < 50) & (t.trip_seconds > 60) & (t.trip_seconds < 3 * 3600) & (t.fare > 0) & (t.fare < 200)]
rng = np.random.default_rng(42)
test = rng.random(len(t)) < 0.2
X = np.column_stack([np.ones(len(t)), t.trip_miles, t.trip_seconds / 60])
y = t.fare.to_numpy()
w, *_ = np.linalg.lstsq(X[~test], y[~test], rcond=None)
pred = X[test] @ w
r2 = 1 - ((y[test] - pred) ** 2).sum() / ((y[test] - y[test].mean()) ** 2).sum()
mae = np.abs(y[test] - pred).mean()
print(f"training rows {int((~test).sum())}, evaluation rows {int(test.sum())}")
print(f"fare = {w[0]:.2f} + {w[1]:.2f} x miles + {w[2]:.2f} x minutes")
print(f"evaluation: r2 {r2:.3f}, mean absolute error ${mae:.2f}")
