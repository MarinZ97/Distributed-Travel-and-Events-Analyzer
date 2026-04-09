import polars as pl
from config import ACCOMMODATIONS_DATASET_PATH


def summarize_accommodations(city: str, date_from: str, date_to: str):
    try:
        df = pl.read_csv(ACCOMMODATIONS_DATASET_PATH)
    except Exception as e:
        print(f"Accommodations dataset error: {e}")
        return None, "Accommodations dataset could not be loaded"

    filtered = df.filter(
        pl.col("destination_city").str.to_lowercase() == city.lower()
    )

    if filtered.height == 0:
        return None, f"No accommodation options found for city: {city}"

    cheapest_options = (
        filtered.sort("price_per_stay")
        .select(
            [
                "hotel_name",
                "destination_city",
                "area",
                "price_per_stay",
                "rating_score",
                "stars",
                "breakfast",
            ]
        )
        .head(5)
        .to_dicts()
    )

    summary = {
        "destination_city": city,
        "count": filtered.height,
        "min_price_per_stay": filtered["price_per_stay"].min(),
        "avg_price_per_stay": round(filtered["price_per_stay"].mean(), 2),
        "avg_rating_score": round(filtered["rating_score"].mean(), 2),
        "top_cheapest_options": cheapest_options,
    }

    return summary, "Accommodation options processed successfully"