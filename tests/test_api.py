def test_analyze_pr(client):
    response = client.post("/analyze-pr", json={
        "repo": "octocat/Hello-World",
        "pr_number": 42
    })
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_status_invalid(client):
    response = client.get("/status/invalid-task-id")
    assert response.status_code == 404

def test_results_invalid(client):
    response = client.get("/results/invalid-task-id")
    assert response.status_code == 404
