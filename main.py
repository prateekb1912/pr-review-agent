# main.py
from fastapi import FastAPI
from celery.result import AsyncResult
from celery_app import analyze_pr_task
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/analyze-pr")
def analyze_pr(request: dict):
    task = analyze_pr_task.delay(request["pr_url"])
    logger.info(f"Analyzing PR {request['pr_url']}. Task id: {task.id}")
    return {"task_id": task.id}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id)
    logger.info(f"Status for task {task_id}: {result.status}")
    return {
        "task_id": task_id, 
        "status": result.status, 
        "result": result.result
    }

@app.get("/results/{task_id}")
def get_results(task_id: str):
    result = AsyncResult(task_id)
    if result.status == "SUCCESS":
        logger.info(f"Results for task {task_id}: {result.result}")
        return result.result
    else:
        logger.info(f"No results for task {task_id}")
        return None