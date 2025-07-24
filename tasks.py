from celery_app import celery_app
import time

@celery_app.task(bind=True)
def analyze_pr_task(repo_url: str, pr_number: int):
    time.sleep(5)
    return {
        "repo_url": repo_url,
        "pr_number": pr_number,
        "status": "success",
        "message": "PR analyzed successfully"
    }