import pytest
import os
from app.services.scanner.git_scanner import GitScanner
from app.services.scanner.dependency_parser import DependencyParser

def test_dependency_parser_package_json():
    content = '{"dependencies": {"react": "^18.2.0"}, "devDependencies": {"typescript": "^5.0.0"}}'
    deps = DependencyParser.parse_package_json(content)
    assert len(deps) == 2
    assert deps[0]["name"] == "react"

def test_dependency_parser_pyproject():
    content = '[project]\ndependencies = ["fastapi>=0.110.0", "uvicorn"]'
    deps = DependencyParser.parse_pyproject_toml(content)
    assert len(deps) == 2
    assert deps[0]["name"] == "fastapi"

def test_dependency_parser_requirements():
    content = "pyjwt==2.8.0\n# comment\nrequests>=2.31.0"
    deps = DependencyParser.parse_requirements_txt(content)
    assert len(deps) == 2
    assert deps[0]["name"] == "pyjwt"

def test_git_scanner(tmp_path):
    p = tmp_path / "sample.py"
    p.write_text("def hello(): pass")
    scanner = GitScanner(str(tmp_path))
    res = scanner.scan()
    assert len(res["files"]) >= 1
