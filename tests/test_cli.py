from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from easyignore.main import app

runner = CliRunner()


@pytest.fixture()
def get_path():
    return Path(__file__).parent.resolve()


def test_app():
    result = runner.invoke(app, ["python", "-o"])
    assert result.exit_code == 0
    assert Path(__file__).parent.joinpath(".gitignore").exists()


def test_multiple_args():
    result = runner.invoke(app, ["python", "node", "-o"])
    assert result.exit_code == 0
    assert Path(__file__).parent.joinpath(".gitignore").exists()
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
    assert not Path(__file__).parent.joinpath(".gitignore").exists()


def test_help():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0


def test_prettier():
    result = runner.invoke(
        app,
        [
            "python",
            "-r",
        ],
    )
    assert result.exit_code == 0
    assert Path(__file__).parent.joinpath(".prettierignore").exists()
    result = runner.invoke(app, ["python", "--overwrite", "--prettier"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--append", "--prettier"])
    assert result.exit_code == 0


def test_append():
    result = runner.invoke(app, ["python", "-a"])
    assert result.exit_code == 0
    assert Path(__file__).parent.joinpath(".gitignore").exists()
    result = runner.invoke(app, ["python", "--append"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o", "-a"])
    assert result.exit_code == 2
    assert "Invalid value for 'append' / 'overwrite'" in result.stdout


def test_overwrite():
    result = runner.invoke(app, ["python", "-o"])
    assert result.exit_code == 0
    assert Path(__file__).parent.joinpath(".gitignore").exists()
    result = runner.invoke(app, ["python", "--overwrite"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-a", "-o"])
    assert result.exit_code == 2
    assert "Invalid value for 'append' / 'overwrite'" in result.stdout


def test_list():
    result = runner.invoke(app, ["python", "-l"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--list"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o", "-l"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--overwrite", "--list"])
    assert result.exit_code == 0
    assert not Path(__file__).parent.joinpath(".gitignore").exists()


def test_path():
    path = str(Path(__file__).resolve().parent)
    # first test with no overwrite - should work since the file doesn't exist
    result = runner.invoke(app, ["python", "-p", path])
    assert result.exit_code == 0
    assert Path(__file__).parent.joinpath(".gitignore").exists()
    # subsequent tests need to overwrite
    result = runner.invoke(app, ["python", "-o", "-p", path])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--overwrite", "--path", path])
    assert result.exit_code == 0


def test_no_options():
    result = runner.invoke(app, ["python"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python"], input="a")
    assert result.exit_code == 0
    result = runner.invoke(app, ["python"], input="o")
    assert result.exit_code == 0
    result = runner.invoke(app, ["python"], input="c")
    assert result.exit_code == 1
