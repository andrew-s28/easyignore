from __future__ import annotations

from pathlib import Path

import pytest
import typer

from easyignore.main import (
    get_file_type_links,
    get_gitignore,
    get_gitignores,
    main,
    validate_gitignores,
)


@pytest.fixture()
def example_gitignore():
    path = Path("testdata/.gitignore")
    return path.read_text()


def test_get_gitignore(example_gitignore):
    languages = ["python"]
    gitignore = get_gitignore(languages)
    assert gitignore == example_gitignore


def test_get_gitignores():
    gitignores = get_gitignores()
    assert isinstance(gitignores, list)
    assert len(gitignores) > 0
    assert "python" in gitignores
    assert "node" in gitignores
    assert "react" in gitignores
    assert "c++" in gitignores
    assert "rust" in gitignores
    assert "csharp" in gitignores


def test_validate_gitignores():
    languages = ["python", "node", "react"]
    invalid_lang = "invalidlang"
    assert validate_gitignores(languages) == languages
    with pytest.raises(typer.BadParameter):
        validate_gitignores([invalid_lang])


def test_get_file_type_links():
    language = ["python"]
    assert get_file_type_links(language) == "[bold][link=https://gitignore.io/api/python]python[/link][/bold]"
    languages = ["python", "node"]
    assert (
        get_file_type_links(languages)
        == "[bold][link=https://gitignore.io/api/python]python[/link][/bold] and [bold][link=https:///gitignore.io/api/node]node[/link][/bold]"
    )
    languages = ["python", "node", "react"]
    assert (
        get_file_type_links(languages)
        == "[link=https://gitignore.io/api/python]python[/link], [link=https://gitignore.io/api/node]node[/link], and [bold][link=https://gitignore.io/api/react]react[/link][/bold]"
    )


def test_main(example_gitignore):
    languages = ["python"]
    gitignore = main(languages)
    gitignore = Path(".").joinpath(".gitignore").read_text()
    assert gitignore == example_gitignore
