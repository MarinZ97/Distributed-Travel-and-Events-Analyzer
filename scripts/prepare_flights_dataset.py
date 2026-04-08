import polars as pl
from pathlib import Path

RAW_PATH = Path ("data/raw/flights/europe_air_routes.csv")
OUTPUT_PATH = Path("datasets/flights.csv")

def main():
    df = pl.read_csv(RAW_PATH, infer_schema_length = 1000)

    prepared = (
        df.select(
            [
                pl.col("departure_city").alias("departure_city"),
                pl.col("arrival_airport_city_name_en").alias("destination_city"),
                pl.col("iata_from").alias("departure_airport"),
                pl.col("iata_to").alias("arrival_airport"),
                pl.col("arrival_airport_country_code").alias("destination_country_code"),
                pl.col("price").alias("price"),
                pl.col("common_duration").alias("duration_minutes"),
                pl.col("flights_per_day").alias("flights_per_day"),
                pl.col("flights_per_week").alias("flights_per_week"),
                pl.col("first_flight").alias("first_flight"),
                pl.col("last_flight").alias("last_flight"),
            ]
        )
        .filter(pl.col("destination_city").is_not_null())
        .filter(pl.col("departure_city").is_not_null())
        .filter(pl.col("price").is_not_null())
        .filter(pl.col("price") > 0)
        .unique()
        .sort(["destination_city", "price"])
    )

    OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)
    prepared.write_csv(OUTPUT_PATH)

    print(f"Prepared flights datasets are saved to: {OUTPUT_PATH}")
    print(f"Rows: {prepared.height}")
    print(f"Columns: {prepared.columns}")

if __name__ == "__main__":
    main()