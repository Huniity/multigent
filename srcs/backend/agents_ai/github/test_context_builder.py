import tempfile
import os
import pytest

from agents_ai.github.context_builder import (
    build_context_from_file,
    build_context_from_pasted_code,
)


#  build_context_from_file


def test_build_context_from_file_returns_bundle():
    files = [
        {"name": "foo.py", "content": "print('hello')"},
        {"name": "bar.py", "content": "x = 1"},
    ]
    result = build_context_from_file(files)
    assert "foo.py" in result["code_bundle"]
    assert "print('hello')" in result["code_bundle"]
    assert "bar.py" in result["code_bundle"]


def test_build_context_from_file_returns_file_names():
    files = [{"name": "a.py", "content": "pass"}]
    result = build_context_from_file(files)
    assert result["files_included"] == ["a.py"]


def test_build_context_from_file_empty_list():
    result = build_context_from_file([])
    assert result["code_bundle"] == ""
    assert result["files_included"] == []


# build_context_from_pasted_code


def test_build_context_from_pasted_code_returns_code():
    code = "def foo():\n    return 42"
    result = build_context_from_pasted_code(code)
    assert result["code_bundle"] == code


def test_build_context_from_pasted_code_files_included_empty():
    result = build_context_from_pasted_code("some code")
    assert result["files_included"] == []


def test_build_context_from_pasted_code_empty_string():
    result = build_context_from_pasted_code("")
    assert result["code_bundle"] == ""
