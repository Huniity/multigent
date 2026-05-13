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