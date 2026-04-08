import polars as pl
try:
    from .config import FLIGHTS_DATASET_PATH
except ImportError:
    from config import FLIGHTS_DATASET_PATH

def summarize_flights(city: str, date_from: str, date_to: str):
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

    cheapest_options = (
        filtered.sort("price").select (
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
        .head(5)
        .to_dicts()
    )

    summary = {
        "destination_city": city,
        "count": filtered.height,
        "min_price": filtered["price"].min(),
        "avg_price": filtered["price"].mean(),
        "min_duration_minutes": filtered["duration_minutes"].min(),
        "avg_duration_minutes": filtered["duration_minutes"].mean(),
        "top_cheapest_options": cheapest_options,
    }

    return summary, "Flight options processed successfully"