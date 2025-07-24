import os
from celery import Celery

from agent.crew_runner import run_code_review
from agent.tools.github import fetch_pr_diff

from dotenv import load_dotenv

load_dotenv()

# Get Redis URL from environment variables
REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379/0"

celery_app = Celery(
    "review_agent",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Configure Celery
celery_app.conf.update(
    result_backend=REDIS_URL,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True)
def analyze_pr_task(self, pr_url: str):
    repo_url, pr_number = pr_url.split("/pull/")
    diff, pr_title, pr_description = fetch_pr_diff(repo_url, int(pr_number))
    review_result = run_code_review(diff, pr_title, pr_description)
    res = {
        "pr_url": pr_url,
        "status": "success",
        "message": "PR analyzed successfully",
        "review": review_result
    }

    return res