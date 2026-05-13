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