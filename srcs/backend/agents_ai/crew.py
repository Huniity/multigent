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