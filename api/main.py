from fastapi import FastAPI, HTTPException
import uuid
import logging
from schemas import TravelRequest, JobCreatedResponse, JobStatusResponse, JobResultResponse
from models import  JobStatus
from store import JOBS
from config import TICKETMASTER_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Distributed Travel and Events Analyzer",
    description="Master API service for distributed travel and events analysis",
    version="0.1.0"
)

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


@app.post("/requests", response_model=JobCreatedResponse, tags=["requests"])
def create_request(request: TravelRequest):
    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "status": JobStatus.PENDING,
        "request": request.model_dump(),
        "result": None
    }
    
    logger.info(f"Created job {job_id} for city={request.city}")
    return {"job_id": job_id}

@app.get("/requests/{job_id}", response_model=JobStatusResponse, tags=["requests"])
def get_request_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"job_id": job_id, "status": job["status"]}

@app.get("/requests/{job_id}/result", response_model=JobResultResponse, tags=["requests"])
def get_request_result(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Dummy result for now
    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job["result"]
    }

@app.get("/config")
def config_info():
    return {
        "ticketmaster_configured": TICKETMASTER_API_KEY != ""
    }



