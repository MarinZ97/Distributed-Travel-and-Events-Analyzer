import polars as pl
try:
    from .config import FLIGHTS_DATASET_PATH
except ImportError:
    from config import FLIGHTS_DATASET_PATH

def summarize_flights(city: str, date_from: str, date_to: str, sort_mode: str = "cheapest", limit: int = 5):
    try:
        df = pl.read_csv(FLIGHTS_DATASET_PATH)
    except Exception as e:
        print(f"Flights dataset error: {e}")
        return None, "Flights dataset could not be loaded"

    # Pretpostavimo da CSV ima kolone:
    # destination_city, departure_date, price

    filtered = df.filter(pl.col("destination_city").str.to_lowercase() == city.lower())
    if filtered.height == 0:
        return None, "No flight data found for given city and perid"

    selected = filtered.select (
            [
                "departure_city",
                "destination_city",
                "departure_airport",
                "arrival_airport",
                "price",
                "duration_minutes",
                "flights_per_day",
                "flights_per_week",
            ]
    )

    if sort_mode == "expensive":
        sorted_options = selected.sort("price", descending=True)
        note = "Flight options processed successfully (sorted by highest price)"
    else:
        sorted_options = selected.sort("price")
        note = "Flight options processed successfully (sorted by lowest price)"

    top_options = sorted_options.head(limit).to_dicts()

    summary = {
        "destination_city": city,
        "count": filtered.height,
        "min_price": filtered["price"].min(),
        "avg_price": round(filtered["price"].mean(), 2),
        "min_duration_minutes": filtered["duration_minutes"].min(),
        "avg_duration_minutes": round(filtered["duration_minutes"].mean(), 2),
        "sort_mode": sort_mode,
        "options_limit": limit,
        "top_options": top_options,
    }

    return summary, note