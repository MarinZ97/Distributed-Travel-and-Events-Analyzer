from pydantic import BaseModel
from datetime import date
from models import JobStatus
from typing import Any, Optional

class TravelRequest(BaseModel):
    city: str
    date_from: date
    date_to: date

class JobCreatedResponse(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus

class JobResultResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Optional[Any] = None
