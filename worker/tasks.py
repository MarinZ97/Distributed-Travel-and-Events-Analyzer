import time
from celery_app import celery_app
from ticketmaster_client import fetch_events


@celery_app.task(name="process_travel_request", bind=True)
def process_travel_request(self, payload: dict) -> dict:
    self.update_state(state="STARTED")

    city = payload.get("city")
    date_from = payload.get("date_from")
    date_to = payload.get("date_to")

    events = fetch_events(city=city, date_from=date_from, date_to=date_to, size=20)

    # 10 sec for simulation
    time.sleep(10)

    return {
        "city": city,
        "date_from": date_from,
        "date_to": date_to,
        "events": events,
        "flights_summary": None,
        "accommodations_summary": None,
        "note": "Ticketmaster events fetched (if API key set)"
    }
