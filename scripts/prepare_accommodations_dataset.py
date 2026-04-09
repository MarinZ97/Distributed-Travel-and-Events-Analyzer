from pathlib import Path
import polars as pl

RAW_PATH = Path("data/raw/accommodations/all_hotels.csv")
OUTPUT_PATH = Path("datasets/accommodations.csv")


def main():
    df = pl.read_csv(
        RAW_PATH,
        infer_schema_length = 10000,
        ignore_errors = True,
    )

    unnamed_cols = [col for col in df.columns if col.strip() == ""]
    if unnamed_cols:
        df = df.drop(unnamed_cols)

    prepared = (
        df.rename(
            {
                "Hotel name": "hotel_name",
                "Marks": "rating_score",
                "Region City": "region_city",
                "Price": "price_raw",
                "Performances": "performances",
                "Reviews": "reviews",
                "Distances": "distance",
                "Discriptions": "description",
                "Stars": "stars",
                "Breakfast": "breakfast",
                "Guests reviews:": "guest_reviews",
            }
        )
        .with_columns(
            [
                pl.col("price_raw")
                .cast(pl.Utf8)
                .str.replace_all(r"[^\d]", "")
                .cast(pl.Int64, strict = False)
                .alias("price_per_stay"),

                pl.col("region_city")
                .cast(pl.Utf8)
                .str.split(",")
                .list.first()
                .str.strip_chars()
                .alias("area"),

                pl.col("region_city")
                .cast(pl.Utf8)
                .str.split(",")
                .list.last()
                .str.strip_chars()
                .alias("destination_city"),
            ]
        )
        .filter(pl.col("hotel_name").is_not_null())
        .filter(pl.col("destination_city").is_not_null())
        .filter(pl.col("price_per_stay").is_not_null())
        .filter(pl.col("price_per_stay") >= 30)
        .filter(pl.col("price_per_stay") <= 10000)
        .select(
            [
                "hotel_name",
                "destination_city",
                "area",
                "price_per_stay",
                "rating_score",
                "stars",
                "breakfast",
                "distance",
                "description",
                "reviews",
                "guest_reviews",
            ]
        )
        .unique(subset=["hotel_name", "destination_city", "price_per_stay"])
        .sort(["destination_city", "price_per_stay"])
    )


    OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)
    prepared.write_csv(OUTPUT_PATH)

    print(f"Prepared accommodations dataset saved to: {OUTPUT_PATH}")
    print(f"Rows: {prepared.height}")
    print(f"Columns: {prepared.columns}")


if __name__ == "__main__":
    main()