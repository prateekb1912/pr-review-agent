import os
from celery import Celery
import time

celery_app = Celery(
    "review_agent",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)

@celery_app.task(bind=True)
def analyze_pr_task(self, repo_url: str, pr_number: int):
    time.sleep(10)

    res = {
        "repo_url": repo_url,
        "pr_number": pr_number,
        "status": "success",
        "message": "PR analyzed successfully"
    }

    return res