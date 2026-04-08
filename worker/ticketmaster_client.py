import os
import requests
from datetime import datetime
from config import TICKETMASTER_API_KEY

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def to_iso_start(date_str: str) -> str:
    dt = datetime.fromisoformat(date_str).replace(hour=0, minute=0, second=0)
    return dt.isoformat() + "Z"


def to_iso_end(date_str: str) -> str:
    dt = datetime.fromisoformat(date_str).replace(hour=23, minute=59, second=59)
    return dt.isoformat() + "Z"


def fetch_events(city: str, date_from: str, date_to: str, size: int = 20):
    if not TICKETMASTER_API_KEY:
        return [], "Ticketmaster API is not configured"

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": city,
        "startDateTime": to_iso_start(date_from),
        "endDateTime": to_iso_end(date_to),
        "size": size,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Ticketmaster API error: {e}")
        return [], f"Ticketmaster API error: {e}"

    events_raw = data.get("_embedded", {}).get("events", [])

    if not events_raw:
        return [], "No events found for given city and period"

    events = []

    for event in events_raw:
        events.append({
            "name": event.get("name"),
            "date": event.get("dates", {}).get("start", {}).get("localDate"),
            "time": event.get("dates", {}).get("start", {}).get("localTime"),
            "venue": event.get("_embedded", {}).get("venues", [{}])[0].get("name"),
            "city": event.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
            "url": event.get("url"),
        })

    return events, "Ticketmaster events fetched successfully" 
