from __future__ import annotations

from typer.testing import CliRunner

from easyignore.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["python", "-o"])
    assert result.exit_code == 0


def test_multiple_args():
    result = runner.invoke(app, ["python", "node", "-o"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "node", "react", "-o"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "c++", "rust", "csharp", "-o"])
    assert result.exit_code == 0


def test_invalid_args():
    result = runner.invoke(app, ["python", "node", "invalidlang"])
    assert result.exit_code == 2
    # test for notification of invalid language
    assert "Invalid value for 'LANGUAGES...': Invalid language: invalidlang" in result.stdout
    # test for generating close matches
    assert "pythonvanilla, leiningen, xilinx, vivado, vaadin" in result.stdout


def test_help():
    result = runner.invoke(app, [])
    print(result.stdout)
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS] LANGUAGES..." in result.stdout
    assert "Arguments" in result.stdout
    assert "--path" in result.stdout
    assert "--append" in result.stdout
    assert "--overwrite" in result.stdout
    assert "--prettier" in result.stdout
    assert "--list" in result.stdout
    assert "--help" in result.stdout
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS] LANGUAGES..." in result.stdout
    assert "Arguments" in result.stdout
    assert "--path" in result.stdout
    assert "--append" in result.stdout
    assert "--overwrite" in result.stdout
    assert "--prettier" in result.stdout
    assert "--list" in result.stdout
    assert "--help" in result.stdout
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS] LANGUAGES..." in result.stdout
    assert "Arguments" in result.stdout
    assert "--path" in result.stdout
    assert "--append" in result.stdout
    assert "--overwrite" in result.stdout
    assert "--prettier" in result.stdout
    assert "--list" in result.stdout
    assert "--help" in result.stdout


def test_optional_args():
    result = runner.invoke(app, ["python", "-a"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--append"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--overwrite"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o", "-p", "."])
    print(result.stdout)
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o", "--path", "."])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-l"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--list"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o", "-r"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o", "--prettier"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-h"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--help"])
    assert result.exit_code == 0


def test_combined_optional_args():
    result = runner.invoke(app, ["python", "-a", "-o"])
    assert result.exit_code == 2
    assert "Invalid value for 'append' / 'overwrite'" in result.stdout
