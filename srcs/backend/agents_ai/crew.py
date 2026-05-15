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
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential, 
            verbose=True
        )