from crewai import Crew
from agent.agents import code_reviewer
from agent.tasks import create_code_review_task

def run_code_review(diff, pr_title, pr_description):
    task = create_code_review_task(diff, pr_title, pr_description)
    task.agent = code_reviewer

    crew = Crew(
        agents=[code_reviewer],
        tasks=[task],
        verbose=True,
    )
    result = crew.kickoff()
    return result
