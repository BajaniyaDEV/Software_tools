from pathlib import Path
import time

import pandas as pd
import polars as pl


csv_file = Path(__file__).parent / "yellow_tripdata_2019-01.csv"

# Pandas
start = time.time()
df_pd = pd.read_csv(csv_file, nrows=100_000)
result_pd = df_pd[df_pd["passenger_count"] > 2]["total_amount"].mean()
print("Pandas result:", result_pd)
print("Pandas execution time:", time.time() - start, "seconds")

# Polars
start = time.time()
df_pl = pl.read_csv(csv_file, n_rows=100_000)
result_pl = (
    df_pl.filter(pl.col("passenger_count") > 2)
    .select(pl.col("total_amount").mean())
)
print("Polars result:", result_pl)
print("Polars execution time:", time.time() - start, "seconds")
