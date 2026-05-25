import re

from pathlib import Path
from typing import List

from concurrent.futures import ThreadPoolExecutor

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
#from crewai_tools import FileReadTool


@CrewBase
class SecurityCrew():
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    
    @agent
    def security_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_analyzer'],
            #tools=[FileReadTool()], 
            verbose=True,
            allow_delegation=False
        )

    @agent
    def performance_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_profiler'],
            #tools=[FileReadTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def bug_detector(self) -> Agent:
        return Agent(
            config=self.agents_config['bug_detector'],
            #tools=[FileReadTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def style_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['style_reviewer'],
            #tools=[FileReadTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def review_leader(self) -> Agent:
        #output_reader_tool = FileReadTool(root_dir='./output')
        return Agent(
            config=self.agents_config['review_leader'],
            #tools=[output_reader_tool],
            verbose=True,
            allow_delegation=False
        )


    @task
    def security_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_audit_task'],
            output_file='output/security_report.md'
        )


    @task
    def bug_detection_task(self) -> Task:
        return Task(
            config=self.tasks_config['bug_detection_task'],
            output_file='output/bug_report.md'
        )

    @task
    def performance_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['performance_analysis_task'],
            output_file='output/performance_report.md'
        )

    @task
    def style_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['style_review_task'],
            output_file='output/style_report.md'
        )

    @task
    def final_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_report_task'],
            output_file='output/final_report.md' 
        )


    @crew
    def crew(self) -> Crew:
        """Cria e junta a equipa na ordem sequencial correta"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,   
            process=Process.sequential, 
            verbose=True
        )

    

    def _read_output(self, filename: str) -> str:
        path = Path(__file__).parent.parent / filename

        if path.exists():
            return path.read_text(encoding='utf-8')
        return ''

    def _parse_score(self, final_report: str) -> int | None:
        match = re.search(r'(?:Overall Health Score|Health Score)[^\d]*(\d{1,3})', final_report)
        if match:
            return int(match.group(1))
        return None

    def _run_crew(self, agent, task, inputs: dict):
        Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        ).kickoff(inputs=inputs)

    def run(self, bundle: dict) -> dict:
        inputs = {
            'code_bundle': bundle['code_bundle'],
            'repo_url': ', '.join(bundle['files_included']) or 'pasted snippet',
        }

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self._run_crew, self.security_analyzer(),    self.security_audit_task(),       inputs),
                executor.submit(self._run_crew, self.bug_detector(),         self.bug_detection_task(),        inputs),
                executor.submit(self._run_crew, self.performance_profiler(), self.performance_analysis_task(), inputs),
                executor.submit(self._run_crew, self.style_reviewer(),       self.style_review_task(),         inputs),
            ]
            for f in futures:
                f.result()

        self._run_crew(self.review_leader(), self.final_report_task(), inputs)

        return {
            'bug_report': self._read_output('output/bug_report.md'),
            'security_report': self._read_output('output/security_report.md'),
            'style_report': self._read_output('output/style_report.md'),
            'performance_report': self._read_output('output/performance_report.md'),
            'final_report': self._read_output('output/final_report.md'),
            'overall_score': self._parse_score(self._read_output('output/final_report.md')),

        }
