# main.py
from fastapi import FastAPI
from celery.result import AsyncResult

from celery_app import analyze_pr_task

app = FastAPI()

@app.post("/analyze-pr")
def analyze_pr(request: dict):
    task = analyze_pr_task.delay(request["repo_url"], request["pr_number"])
    return {"task_id": task.id}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "task_id": task_id, 
        "status": result.status, 
        "result": result.result
    }

@app.get("/results/{task_id}")
def get_results(task_id: str):
    result = AsyncResult(task_id)
    if result.status == "SUCCESS":
        return result.result
    else:
        return None