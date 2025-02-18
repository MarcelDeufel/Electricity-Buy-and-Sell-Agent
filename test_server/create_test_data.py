import pandas as pd
import os

# Load the dataset
base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory where the script is located
file_path = os.path.join(base_path, "../data/Continuous_Orders-DE-20210627-20210628T042307000Z.csv")

df = pd.read_csv(file_path)

# Convert TransactionTime to datetime (if it's not already)
df["TransactionTime"] = pd.to_datetime(df["TransactionTime"], errors="coerce")

# Step 1: Keep only the latest revision for each OrderId
df = df.sort_values(by=["OrderId", "RevisionNo"], ascending=[True, False]).drop_duplicates(subset=["OrderId"], keep="first")

# Step 2: Remove orders that never became a transaction (TransactionTime is NaN)
df = df[df["TransactionTime"].notna()]

# Convert CreationTime and TransactionTime to datetime
df["CreationTime"] = pd.to_datetime(df["CreationTime"], errors="coerce")
df["TransactionTime"] = pd.to_datetime(df["TransactionTime"], errors="coerce")

# Ensure the output directory exists
os.makedirs("interval_data", exist_ok=True)

# Split the dataset into 15-minute intervals and save each interval as a separate CSV file
for day in pd.date_range(df["CreationTime"].min().normalize(), df["CreationTime"].max().normalize(), freq="D"):
    day_data = df[(df["CreationTime"] >= day) & (df["CreationTime"] < day + pd.Timedelta(days=1))]
    
    for interval_start in pd.date_range(day, day + pd.Timedelta(days=1), freq="15T")[:-1]:
        interval_end = interval_start + pd.Timedelta(minutes=15)
        interval_data = day_data[(day_data["CreationTime"] >= interval_start) & (day_data["CreationTime"] < interval_end)]
        
        if not interval_data.empty:
            filename = f"interval_data/{interval_start.strftime('%Y%m%d_%H%M')}.csv"
            interval_data.to_csv(filename, index=False)
            print(f"Saved {filename} with {len(interval_data)} rows.")
