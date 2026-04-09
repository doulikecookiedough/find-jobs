from pathlib import Path

from find_jobs.cli import main


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_main_returns_error_without_command(capsys) -> None:
    assert main([]) == 1

    captured = capsys.readouterr()
    assert "Usage: find-jobs evaluate <job-file>" in captured.out


def test_main_evaluate_command_prints_score_summary(capsys) -> None:
    result = main(["evaluate", str(FIXTURES_DIR / "affirm_backend_engineer.txt")])

    assert result == 0

    captured = capsys.readouterr()
    assert "Title: Software Engineer II, Backend (Consumer Authentication)" in captured.out
    assert "Company: Affirm" in captured.out
    assert "Fit Score:" in captured.out
    assert "Skills Alignment:" in captured.out
    assert "Interview Probability:" in captured.out
    assert "Recommendation: apply" in captured.out
    assert "Priority: high" in captured.out
    assert "Reasons:" in captured.out
    assert "- Role type aligns well with your target focus (backend)." in captured.out
    assert "Parser Warnings:" not in captured.out
