from fastapi import FastAPI
import uuid
import logging
from schemas import TravelRequest, JobCreatedResponse, JobStatusResponse
from models import  JobStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Distributed Travel and Events Analyzer",
    description="Master API service for distributed travel and events analysis",
    version="0.1.0"
)



@app.post("/requests", response_model=JobCreatedResponse)
def create_request(request: TravelRequest):
    job_id = str(uuid.uuid4())
    logger.info(f"Created job {job_id} for city={request.city}")
    return {"job_id": job_id}


@app.get("/requests/{job_id}", response_model=JobStatusResponse)
def get_request_status(job_id: str):
    return {
        "job_id": job_id,
        "status": JobStatus.PENDING
    }

@app.get("/")
def root():
    return {
        "service": "Distributed Travel and Events Analyzer",
        "role": "API (Master)",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "ok"}