from security_crew.crew import SecurityCrew

def run_analysis():

    inputs = {
        'repo_url': 'https://github.com/Huniity/multigent.git',
        'topic': 'Security Vulnerabilities and Secrets'
    }

    print("--- Starting Security Analysis ---")
    result = SecurityCrew().crew().kickoff(inputs=inputs)

    print("## ANALYSIS COMPLETED ##")
    print(result)

if __name__ == "__main__":
    run_analysis()

from agents_ai.agents.tasks import build_bug_task

def start_review():
    my_bundle = build_bug_task(repo_url, readed_files, modified_files, deleted_files)

    inputs = {
        'repo_url': 'https://github.com/Huniity/multigent.git',
        'code_bundle': my_bundle  
    }
    
    SecurityCrew().crew().kickoff(inputs=inputs)
