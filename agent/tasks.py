from crewai import Task

def create_code_review_task(code_diff, pr_title, pr_description):
    description = f"""
        Provide a detailed review of the changes, including any and all suggestions for improvements or fixes.
        If any of the agents find an issue, you should provide a detailed explanation of the issue and a suggestion for a fix.
        If no issues are found, return with "No issues found" for each section.
        The output should have the following format:
        - Bug Fixes:
        - Logic Errors:
        - Style Issues:
        - Best Practices:
        - Security Issues:
        - Verdict:

        The verdict should be one of the following:
        - Approve
        - Needs Changes
        - Needs More Review
        Review the following PR and provide any and all suggestions.
        PR Title: {pr_title}
        PR Description: {pr_description}
        PR Diff:
        {code_diff}
        """
    
    return Task(
        description=description,
        expected_output="Consolidated review with style, bug, performance, and best practices feedback.",
    )
