from app.celery_app import analyze_pr_task

def test_analyze_pull_request_mock(monkeypatch):
    # Setup
    def mock_analyze_pr(self, pr_url: str):
        return {"status": "success", "feedback": "Looks good"}

    monkeypatch.setattr("celery_app.analyze_pr_task", mock_analyze_pr)

    # Act
    result = analyze_pr_task("https://github.com/octocat/Hello-World/pull/42")

    # Assert
    assert result["status"] == "success"
    assert "feedback" in result
