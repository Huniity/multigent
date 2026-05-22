


import tomllib  # Built-in in Python 3.11+
from pathlib import Path

def load_config(config_path="codebase_read_rules.toml"):
    path = Path(config_path)
    
    
    with open(path, "rb") as f:
        config_data = tomllib.load(f)

    return {
        "max_chars_allowed_in_context": config_data.get("max_chars_allowed_in_context", 300000),
        "dirs_to_ignore": set(config_data.get("dirs_to_ignore", [])),
        "extensions_to_ignore": set(config_data.get("extensions_to_ignore", [])),
        "files_to_be_included": set(config_data.get("files_to_be_included", []))
    }


def build_context_from_file(files: list[dict]) -> dict:
    """
    Function to build a context for the crew by reading files from the user input
    """
    code_bundle = ""
    for f in files:
        code_bundle += f"File: {f['name']}\nContent:\n{f['content']}\n\n"

    return {
        "code_bundle": code_bundle,
        "files_included": [f['name'] for f in files]
    }



def build_context_from_pasted_code(pasted_code: str) -> dict:
    """
    Function to build a context for the crew by reading pasted code from the user input
    """

    return {
        "code_bundle": pasted_code,
        "files_included": []
    }


