from crewai import Task

def create_code_review_task(code_diff, pr_title, pr_description):
    return Task(
        description=f"""
        Review the following PR and provide any and all suggestions.
        PR Title: {pr_title}
        PR Description: {pr_description}
        PR Diff:
        {code_diff}
        """,
        expected_output="Consolidated review with style, bug, performance, and best practices feedback."
    )
