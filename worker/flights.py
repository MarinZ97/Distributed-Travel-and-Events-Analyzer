import polars as pl
from config import FLIGHTS_DATASET_PATH

def summarize_flights(city: str, date_from: str, date_to: str):
    try:
        df = pl.read_csv(FLIGHTS_DATASET_PATH)
    except Exception as e:
        print(f"Flights dataset error: {e}")
        return None, "Flights dataset could not be loaded"

    # Pretpostavimo da CSV ima kolone:
    # destination_city, departure_date, price

    filtered = (
        df.filter(pl.col("destination_city") == city)
          .filter(
              (pl.col("departure_date") >= date_from) &
              (pl.col("departure_date") <= date_to)
          )
    )

    if filtered.height == 0:
        return None, "No flight data found for given city and perid"

    return {
        "min_price": filtered["price"].min(),
        "avg_price": filtered["price"].mean(),
        "count": filtered.height
    }
