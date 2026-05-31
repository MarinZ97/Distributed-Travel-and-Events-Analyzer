from datetime import date
from models import JobStatus
from typing import Any, Optional, Literal
from pydantic import BaseModel

class TravelRequest(BaseModel):
    city: str
    departure_city: Optional[str] = None
    date_from: date
    date_to: date
    flight_sort: Literal["cheapest", "expensive"] = "cheapest"
    accommodation_sort: Literal["cheapest", "expensive", "best_rating"] = "cheapest"
    options_limit: Literal[5, 10] = 5

class JobCreatedResponse(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus

class JobResultResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Optional[Any] = None
