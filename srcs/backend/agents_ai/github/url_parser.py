def parse_github_url(url: str) -> tuple[str, str]:
    """
    Extract (owner, repo) from a GitHub URL.
 
    Handles:
      https://github.com/owner/repo
      https://github.com/owner/repo.git
      https://github.com/owner/repo/
    """
    url = url.strip().rstrip("/").removesuffix(".git")
    parts = url.split("/")
 
    if len(parts) < 5 or "github.com" not in parts:
        raise ValueError(
            f"Invalid GitHub URL: '{url}'. "
            "Expected format: https://github.com/owner/repo"
        )
 
    return parts[-2], parts[-1]  # owner, repo
