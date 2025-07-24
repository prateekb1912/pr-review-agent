import os
from celery import Celery
import time

from agent.tools.github import fetch_pr_diff

celery_app = Celery(
    "review_agent",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)

@celery_app.task(bind=True)
def analyze_pr_task(self, pr_url: str):
    repo_url, pr_number = pr_url.split("pull/")
    diff = fetch_pr_diff(repo_url, int(pr_number))
    res = {
        "repo_url": repo_url,
        "pr_number": pr_number,
        "diff": diff,
        "status": "success",
        "message": "PR analyzed successfully"
    }

    return res