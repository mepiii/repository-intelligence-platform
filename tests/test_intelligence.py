from app.services.intelligence.ast_parser import ASTParser

def test_ast_python():
    code = """
class AuthManager:
    """Handles user authentication."""
    def login(self, username, password):
        return True
"""
    res = ASTParser.parse_python(code)
    symbols = res["symbols"]
    assert len(symbols) == 2 # class and method
    assert symbols[0]["name"] == "login" or symbols[1]["name"] == "AuthManager"

def test_ast_typescript():
    code = "import { useState } from 'react';\nclass UserView { render() {} }"
    res = ASTParser.parse_javascript_typescript(code)
    assert len(res["imports"]) == 1
    assert len(res["symbols"]) >= 1
