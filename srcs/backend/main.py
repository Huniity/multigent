
from agents_ai.agents.tasks import build_bug_task

def start_review():
    my_bundle = build_bug_task(repo_url, readed_files, modified_files, deleted_files)

    inputs = {
        'repo_url': 'https://github.com/Huniity/multigent.git',
        'code_bundle': my_bundle  
    }
    
    SecurityCrew().crew().kickoff(inputs=inputs)