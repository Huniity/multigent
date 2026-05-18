from crewai import Agent, Crew, Process, Task
from crewai.project import AgentConfig, CrewBase, TaskConfig, crew, agent
from crewai_tools import FileReadTool  

@CrewBase
class SecurityCrew():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def security_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_analyzer'],
            tools=[FileReadTool()], 
            verbose=True,
            allow_delegation=False  # Prevent delegation to other agents, ensuring the Security Analyzer handles all tasks directly
        )

    @task
    def security_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_audit_task'],
@agent
    def performance_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_profiler'],
            tools=[FileReadTool()],
            verbose=True,
            allow_delegation=False
        )
    

    @task
    def performance_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['performance_analysis_task'],
            output_file='output/performance_report.md'
        )
from crewai import Agent, Crew, Process, Task
from crewai.project import AgentConfig, CrewBase, TaskConfig, crew, agent, task
from crewai_tools import FileReadTool 

@agent
    def review_leader(self) -> Agent:
        output_reader_tool = FileReadTool(root_dir='./output') #root_dir makes the agent focus only on files in the output directory

        return Agent(
            config=self.agents_config['review_leader'],
            tools=[output_reader_tool],
            verbose=True,
            allow_delegation=False
        )

    @task
    def final_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_report_task'],
            output_file='output/final_report.md' 
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Security Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,   
            process=Process.sequential,
            verbose=True,
        )
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential, 
            verbose=True
        )
@task
    def bug_detection_task(self) -> Task:
        return Task(
            config=self.tasks_config['bug_detection_task'],
        )

