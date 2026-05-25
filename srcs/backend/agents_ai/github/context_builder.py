def build_context_from_file(files: list[dict]) -> dict:
    """
    Function to build a context for the crew by reading files from the user input
    """
    code_bundle = ""
    for f in files:
        code_bundle += f"File: {f['name']}\nContent:\n{f['content']}\n\n"

    return {"code_bundle": code_bundle, "files_included": [f["name"] for f in files]}


def build_context_from_pasted_code(pasted_code: str) -> dict:
    """
    Function to build a context for the crew by reading pasted code from the user input
    """

    return {"code_bundle": pasted_code, "files_included": []}
