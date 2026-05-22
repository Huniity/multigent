from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from agents_ai.crew import SecurityCrew
from crewai import LLM
import os


llm = LLM (
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    stream=True
)

class CodeReviewState(BaseModel):
    code_bundle: str = ""
    repo_url: str = "local_analysis"  


class CodeReviewFlow(Flow[CodeReviewState]):

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
    flow = CodeReviewFlow()
    flow.kickoff(inputs={"code_bundle": code})