@task
    def bug_detection_task(self) -> Task:
        return Task(
            config=self.tasks_config['bug_detection_task'],
        )

