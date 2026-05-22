from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
#from crewai_tools import FileReadTool
import yaml
from pathlib import Path

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
        
    def build_bug_task(self, repo_url, list_of_code_files):
        bundle = ""
        for file in list_of_code_files:
            bundle += f"\n--- FILE: {file.get('name', 'unknown')} ---\n"
            bundle += file.get('content', '')
        return bundle


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