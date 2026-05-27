import mlflow
import polars as pl

# %%
print("Q1 start")

from dotenv import load_dotenv

load_dotenv(override=True)
print("Q1 end")
# %%


df = pl.read_parquet("https://minio.lab.sspcloud.fr/projet-formation/diffusion/funathon/2026/project2/generation_None_temp08.parquet")

print(df.head())
print(f"Total rows: {len(df)}")

# %%
n_classes = df['code'].n_unique()
print(f"Number of unique NACE codes: {n_classes}")
# %%

# %%

# %%