import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "")
FLIGHTS_DATASET_PATH = os.getenv("FLIGHTS_DATASET_PATH", "/datasets/flights.csv")