# main.py
from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult

from tasks import analyze_pr_task
from cache import get_task_result

app = FastAPI()

@app.post("/analyze-pr")
def analyze_pr(request: dict):
    task = analyze_pr_task.delay(request["repo_url"], request["pr_number"])
    return {"task_id": task.id}
