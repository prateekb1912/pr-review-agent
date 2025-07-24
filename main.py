# main.py
from fastapi import FastAPI

from celery_app import analyze_pr_task

app = FastAPI()

@app.post("/analyze-pr")
def analyze_pr(request: dict):
    task = analyze_pr_task.delay(request["repo_url"], request["pr_number"])
    return {"task_id": task.id}
