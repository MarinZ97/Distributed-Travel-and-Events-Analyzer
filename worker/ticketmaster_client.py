import os
import requests
from datetime import datetime, time, timezone

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "")
TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def to_iso_start(date_str: str) -> str:
    dt = datetime.fromisoformat(date_str).replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
    )
    return dt.isoformat().replace("+00:00", "Z")


def to_iso_end(date_str: str) -> str:
    dt = datetime.fromisoformat(date_str).replace(
        hour=23, minute=59, second=59, microsecond=0, tzinfo=timezone.utc
    )
    return dt.isoformat().replace("+00:00", "Z")


def fetch_events(city: str, date_from: str, date_to: str, size: int = 20) -> list[dict]:
    """
    Simple Ticketmaster fetch for demo.
    Returns list of events with minimal fields.
    """
    if not TICKETMASTER_API_KEY:
        return []

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": city,
        "startDateTime": to_iso_start(date_from),
        "endDateTime": to_iso_end(date_to),
        "size": size,
        "sort": "date,asc",
    }

    r = requests.get(TM_BASE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    events = []
    embedded = data.get("_embedded", {})
    for e in embedded.get("events", []):
        name = e.get("name")
        url = e.get("url")
        dates = e.get("dates", {}).get("start", {})
        local_date = dates.get("localDate")
        local_time = dates.get("localTime")

        venue_name = None
        venue_city = None
        try:
            venues = e.get("_embedded", {}).get("venues", [])
            if venues:
                venue_name = venues[0].get("name")
                venue_city = venues[0].get("city", {}).get("name")
        except Exception:
            pass

        events.append(
            {
                "name": name,
                "date": local_date,
                "time": local_time,
                "venue": venue_name,
                "city": venue_city,
                "url": url,
            }
        )

    return events
