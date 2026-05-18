


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