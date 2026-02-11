import time
from celery_app import celery_app


@celery_app.task(name="process_travel_request", bind=True)
def process_travel_request(self, payload: dict) -> dict:
    self.update_state(state="STARTED")

    # For testing simulation
    time.sleep(10)

    city = payload.get("city")
    date_from = payload.get("date_from")
    date_to = payload.get("date_to")

    return {
        "city": city,
        "date_from": date_from,
        "date_to": date_to,
        "events": [],
        "flights_summary": None,
        "accommodations_summary": None,
        "note": "worker/queue - OK"
    }
