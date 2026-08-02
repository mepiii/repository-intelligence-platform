from app.services.debt.debt_analyzer import DebtAnalyzer

def test_debt_analyzer():
    content = "def sample(): pass\n" * 350 # Long file
    symbols = [{"name": "sample", "kind": "function", "start_line": 1, "end_line": 100}] # Long function
    report = DebtAnalyzer.analyze_file("legacy.py", content, symbols)
    assert report["debt_score"] > 0
    assert len(report["issues"]) >= 2
