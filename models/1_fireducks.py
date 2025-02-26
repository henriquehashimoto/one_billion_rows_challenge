import fireducks.pandas as pd
import time

start_time = time.time()

df_1billion = pd.read_parquet("/home/henriquehashimoto/git/one_billion_rows_challenge/data/measurements.parquet")

end_time = time.time()
exec_time = end_time - start_time

print(df_1billion.head())

print(f"Tempo de execução: {exec_time} /n/n")


