# main.py
from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from .celery_app import analyze_pr_task, celery_app
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
    try:
        result = AsyncResult(task_id, app=celery_app)
        logger.info(f"Status for task {task_id}: {result.status}")
        return {
            "task_id": task_id, 
            "status": result.status, 
            "result": result.result if result.ready() else None
        }
    except Exception as e:
        logger.error(f"Error getting status for task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving task status: {str(e)}")

@app.get("/results/{task_id}")
def get_results(task_id: str):
    try:
        result = AsyncResult(task_id, app=celery_app)
        if result.status == "SUCCESS":
            logger.info(f"Results for task {task_id}: {result.result}")
            return result.result
        elif result.status == "PENDING":
            logger.info(f"Task {task_id} is still pending")
            return {"status": "pending", "message": "Task is still being processed"}
        elif result.status == "FAILURE":
            logger.error(f"Task {task_id} failed: {result.result}")
            return {"status": "failed", "error": str(result.result)}
        else:
            logger.info(f"No results for task {task_id}, status: {result.status}")
            return {"status": result.status, "message": "Task not completed yet"}
    except Exception as e:
        logger.error(f"Error getting results for task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving task results: {str(e)}")