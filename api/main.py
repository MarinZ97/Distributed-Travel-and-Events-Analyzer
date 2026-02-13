from fastapi import FastAPI, HTTPException
import uuid
import logging
from schemas import TravelRequest, JobCreatedResponse, JobStatusResponse, JobResultResponse
from models import  JobStatus
from store import JOBS
from config import TICKETMASTER_API_KEY
import os
from celery import Celery
from celery.result import AsyncResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_client = Celery(
    "api",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

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



@app.post("/requests", response_model=JobCreatedResponse, tags=["requests"])
def create_request(request: TravelRequest):
    payload = request.model_dump(mode="json")

    task = celery_client.send_task("process_travel_request", args=[payload])

    logger.info(f"Enqueued job {task.id} for city={request.city}")
    return {"job_id": task.id}
    


@app.get("/requests/{job_id}", response_model=JobStatusResponse, tags=["requests"])
def get_request_status(job_id: str):
    result = AsyncResult(job_id, app=celery_client)

    state = result.state

    if state == "PENDING":
        status = JobStatus.PENDING
    elif state in ("STARTED", "RETRY"):
        status = JobStatus.RUNNING
    elif state == "SUCCESS":
        status = JobStatus.DONE
    elif state == "FAILURE":
        status = JobStatus.FAILED
    else:
        status = JobStatus.PENDING

    return {"job_id": job_id, "status": status}
    


@app.get("/requests/{job_id}/result", response_model=JobResultResponse, tags=["requests"])
def get_request_result(job_id: str):
    result = AsyncResult(job_id, app=celery_client)

    if result.state == "PENDING":
        return {"job_id": job_id, "status": JobStatus.PENDING, "result": None}

    if result.state in ("STARTED", "RETRY"):
        return {"job_id": job_id, "status": JobStatus.RUNNING, "result": None}

    if result.state == "FAILURE":
        return {
            "job_id": job_id,
            "status": JobStatus.FAILED,
            "result": {"error": str(result.result)}
        }

    return {
        "job_id": job_id,
        "status": JobStatus.DONE,
        "result": result.get(timeout=1)
    }




@app.get("/config")
def config_info():
    return {
        "ticketmaster_configured": TICKETMASTER_API_KEY != ""
    }



