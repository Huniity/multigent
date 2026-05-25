from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from agents_ai.crew import SecurityCrew
from crewai import LLM
import os


llm = LLM (
    """
    Gemini-2.5-Flash is a powerful language model designed for code analysis and review tasks. 
    """
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    stream=True
)

class CodeReviewState(BaseModel):
    """
    State class for the code review flow, holding the code bundle and repository URL
    """
    code_bundle: str = ""
    repo_url: str = "local_analysis"  


class CodeReviewFlow(Flow[CodeReviewState]):
    """
    Flow class for orchestrating the code review process using the SecurityCrew
    """
    @start()
    def prepare(self, payload: dict | None = None):
        if payload:
            self.state.code_bundle = payload.get("code_bundle", "")
        print(f"Starting analysis on {len(self.state.code_bundle)} chars of code.")

    @listen(prepare)
    def run_crew(self):
        result = SecurityCrew().crew().kickoff(inputs={
            "repo_url": self.state.repo_url,
            "code_bundle": self.state.code_bundle,
        })
        print("Crew finished. Reports written to /output/")


def kickoff(code: str):
    """
    Function to kickoff the code review flow with the provided code bundle
    """
    flow = CodeReviewFlow()
    flow.kickoff(inputs={"code_bundle": code})