import polars as pl
from config import ACCOMMODATIONS_DATASET_PATH

def summarize_accommodations(city: str, date_from: str, date_to: str):
    try:
        df = pl.read_csv(ACCOMMODATIONS_DATASET_PATH)
    except Exception as e:
        print(f"Accommodations dataset error: {e}")
        return None, "Accommodations dataset could not be loaded"


    filtered = (
        df.filter(pl.col("city").str.to_lowercase() == city.lower())
          .filter(
              (pl.col("available_from") <= date_from) &
              (pl.col("available_to") >= date_to)
          )
    )

    if filtered.height == 0:
        return None, "No Accommodations data found for given city and perid"

    cheapest_row = (
        filtered.sort("price_per_night")
        .select(["name", "type", "price_per_night"])
        .row(0, named = True)
    )

    summary = {
        "min_price_per_night": filtered["price_per_night"].min(),
        "avg_price_per_night": filtered["price_per_night"].mean(),
        "count": filtered.height,
        "cheapest_option": cheapest_row,
    }

    return summary, "Accommodation dataset processed successfully"
