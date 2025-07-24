import os
from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=api_key,
    temperature=0.1
)

code_reviewer = Agent(
    role="Expert Code Reviewer",
    goal="Review the given PR diff and provide a detailed review of the changes. Provide a list of suggestions for improvements or fixes.",
    backstory="""
    You are a senior software engineer with an eye for detail. You have an expertise in all major programming languages as well as code linting, formatting, and best practices for all major programming languages.
    You also are a diligent code reviewer who is able to find bugs, logic errors, and style issues in the code.
    """,
    verbose=True,
    llm=llm
)
