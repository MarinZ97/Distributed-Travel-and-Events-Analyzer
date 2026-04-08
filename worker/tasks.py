import time
from celery_app import celery_app
from ticketmaster_client import fetch_events
from flights import summarize_flights
from accommodations import summarize_accommodations


@celery_app.task(name="process_travel_request", bind=True)
def process_travel_request(self, payload: dict) -> dict:
    self.update_state(state="STARTED")

    city = payload.get("city")
    date_from = payload.get("date_from")
    date_to = payload.get("date_to")

    events, events_note = fetch_events(city=city, date_from=date_from, date_to=date_to, size=20)
    flights_summary, flights_note = summarize_flights(city, date_from, date_to)
    accommodations_summary, accommodations_note = summarize_accommodations(city, date_from, date_to)

    # 10 sec for simulation
    time.sleep(10)


    return {
        "city": city,
        "date_from": date_from,
        "date_to": date_to,
        "events": events,
        "flights_summary": flights_summary,
        "accommodations_summary": accommodations_summary,
        "notes": {
            "events": events_note,
            "flights": flights_note,
            "accommodations": accommodations_note,
        },
    }