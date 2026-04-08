import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOCAL_FLIGHTS_PATH = BASE_DIR / "datasets" / "flights.csv"
DOCKER_FLIGHTS_PATH = Path("/datasets/flights.csv")

LOCAL_ACCOMMODATIONS_PATH = BASE_DIR / "datasets" / "accommodations.csv"
DOCKER_ACCOMMODATIONS_PATH = Path("/datasets/accommodations.csv")

if DOCKER_FLIGHTS_PATH.exists():
    default_flights_path = str(DOCKER_FLIGHTS_PATH)
else:
    default_flights_path = str(LOCAL_FLIGHTS_PATH)

if DOCKER_ACCOMMODATIONS_PATH.exists():
    default_accommodations_path = str(DOCKER_ACCOMMODATIONS_PATH)
else:
    default_accommodations_path = str(LOCAL_ACCOMMODATIONS_PATH)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "")
FLIGHTS_DATASET_PATH = os.getenv("FLIGHTS_DATASET_PATH", default_flights_path)
ACCOMMODATIONS_DATASET_PATH = os.getenv("ACCOMMODATIONS_DATASET_PATH" ,default_accommodations_path)