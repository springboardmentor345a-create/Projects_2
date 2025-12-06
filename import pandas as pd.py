import pandas as pd

# Load the dataset
match_df = pd.read_csv("data/Match Winner.csv")

# View first 5 rows
print(match_df.head())

# Check dataset info (columns, data types, nulls)
print(match_df.info())

# Summary statistics
print(match_df.describe())
