from fastapi import FastAPI
from datetime import datetime, timezone, timedelta
import pandas as pd
import os

app = FastAPI()

# Set the initial start time when the server starts
SERVER_START_TIME = datetime.utcnow().replace(tzinfo=timezone.utc)

# Define the two reference days
DAY_1 = "20210626"
DAY_2 = "20210627"

def get_relevant_data(current_time: datetime):
    current_time = current_time.replace(tzinfo=timezone.utc)

    # Calculate how long the server has been running
    time_elapsed = current_time - SERVER_START_TIME
    days_running = int(time_elapsed.total_seconds() // 86400)  # Convert seconds to days

    # Determine which dataset day to use
    selected_day = DAY_1 if days_running % 2 == 0 else DAY_2

    relevant_offers = []

    # Round down current_time to the last 15-minute interval
    interval_start = current_time.replace(second=0, microsecond=0, minute=(current_time.minute // 15) * 15)

    # Format filename using the rounded interval start
    interval_filename = f"interval_data/{selected_day}_{interval_start.strftime('%H%M')}.csv"

    # Check if the file exists
    if os.path.exists(interval_filename):
        df = pd.read_csv(interval_filename)
        df["CreationTime"] = pd.to_datetime(df["CreationTime"], errors="coerce")
        df["TransactionTime"] = pd.to_datetime(df["TransactionTime"], errors="coerce")

        # Filter orders that match the 15-minute interval within the selected day
        filtered_offers = df[
            (df["CreationTime"].dt.hour == current_time.hour) & 
            (df["CreationTime"].dt.minute // 15 == current_time.minute // 15) & 
            ((df["TransactionTime"].isna()) | (df["TransactionTime"] > current_time))
        ]

        if not filtered_offers.empty:
            # Replace NaN with 0 for numeric columns, None for non-numeric
            for col in filtered_offers.columns:
                if filtered_offers[col].dtype.kind in 'fi':  # Numeric types (float, int)
                    filtered_offers[col].fillna(0, inplace=True)
                else:
                    filtered_offers[col].fillna(0, inplace=True)

            relevant_offers.extend(filtered_offers.to_dict(orient="records"))

    return relevant_offers


# API endpoint to get current offers
@app.get("/orders")
def get_orders():
    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)  # Ensure UTC timezone-aware datetime
    relevant_offers = get_relevant_data(current_time)
    return {"current_time": current_time.isoformat(), "selected_day": SERVER_START_TIME.isoformat(), "offers": relevant_offers}
