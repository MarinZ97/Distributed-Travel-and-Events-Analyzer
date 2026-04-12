import polars as pl
from config import ACCOMMODATIONS_DATASET_PATH


def summarize_accommodations(city: str, date_from: str, date_to: str, sort_mode: str= "cheapest", limit: int = 5):
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

    selected = filtered.select(
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
    
    if sort_mode == "expensive":
        sorted_options = selected.sort("price_per_stay", descending = True)
        note = "Accommodation options processed successfully (sorted by highest price)"
    elif sort_mode == "best_rating":
        sorted_options = selected.sort(
            by = ["rating_score", "stars", "price_per_stay"],
            descending = [True, True, False],
        )
        note = "Accommodation options processed successfully (sorted by best rating)"
    else:
        sorted_options = selected.sort("price_per_stay")
        note = "Accommodation options processed successfully (sorted by lowest price)"

    top_options = sorted_options.head(limit).to_dicts()

    summary = {
        "destination_city": city,
        "count": filtered.height,
        "min_price_per_stay": filtered["price_per_stay"].min(),
        "avg_price_per_stay": round(filtered["price_per_stay"].mean(), 2),
        "avg_rating_score": round(filtered["rating_score"].mean(), 2),
        "sort_mode": sort_mode,
        "options_limit": limit,
        "top_options": top_options,
    }

    return summary, note