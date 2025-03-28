import re
from difflib import get_close_matches
from pathlib import Path
from typing import Annotated

import requests
import typer
import typer.completion
from rich import print as rprint
from rich.columns import Columns
from rich.prompt import Prompt

app = typer.Typer(
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
    rich_markup_mode="rich",
    rich_help_panel=True,
    no_args_is_help=True,
    help="Create a .gitignore or .prettierignore file for over 500 languages and frameworks. Currently, the source for the ignore files is https://gitignore.io but this may change in the future to ensure the most up-to-date ignore files are used (see also https://github.com/toptal/gitignore.io/issues/650)",
)


def get_file_type_links(languages: list[str]) -> str:
    if len(languages) == 1:
        return f"[bold][link=https://gitignore.io/api/{languages[0]}]{languages[0]}[/link][/bold]"
    elif len(languages) == 2:
        return f"[bold][link=https://gitignore.io/api/{languages[0]}]{languages[0]}[/link][/bold] and [bold][link=https:///gitignore.io/api/{languages[1]}]{languages[1]}[/link][/bold]"
    elif len(languages) > 2:
        languages_str = ", ".join([f"[link=https://gitignore.io/api/{ft}]{ft}[/link]" for ft in languages[:-1]])
        return (
            f"{languages_str}, and [bold][link=https://gitignore.io/api/{languages[-1]}]{languages[-1]}[/link][/bold]"
        )


def get_gitignore(languages: list[str]) -> str:
    languages = ",".join([f"{ft}" for ft in languages])
    response = requests.get(f"https://gitignore.io/api/{languages}")
    if response.status_code == 200:
        return f"# Created with easyignore\n{response.text}"
    else:
        rprint(
            f"[red]Failed to fetch gitignore for {languages}. Check that {languages} is valid and that you are connected to the internet and try again.[/red]"
        )
        raise typer.Exit(code=1)


def get_gitignores() -> list[str]:
    response = requests.get("https://gitignore.io/api/list")
    if response.status_code == 200:
        return re.split("\n|,", response.text)
    else:
        rprint("[red]Failed to fetch gitignore list. Check your internet connection and try again.[/red]")
        raise typer.Exit(code=1)


def complete_gitignores() -> list[str]:
    return get_gitignores()


def validate_gitignores(value: str) -> str:
    for v in value:
        if v not in complete_gitignores():
            best_matches = get_close_matches(v, complete_gitignores(), n=5, cutoff=0)
            if best_matches:
                raise typer.BadParameter(f"Invalid language: {v}. Perhaps you meant one of: {', '.join(best_matches)}.")
            else:
                raise typer.BadParameter(f"Invalid language: {v}. No close matches found.")
    return value


def list_gitignores(value: bool) -> None:
    """
    List available languages/frameworks available from gitignore.io
    """
    if not value:
        return
    git_ignores = get_gitignores()
    git_ignores = [f"[blue][link=https://gitignore.io/api/{g}]{g}[/link][/blue]" for g in git_ignores]
    git_ignores = Columns(git_ignores, equal=True, expand=True)
    rprint("[bold]Available languages/frameworks for .gitignore:[/bold]")
    rprint(git_ignores)
    raise typer.Exit(code=0)


@app.command(no_args_is_help=True)
def main(
    languages: Annotated[
        list[str],
        typer.Argument(
            help="language/framework for .gitignore (enter as many as you like)",
            autocompletion=complete_gitignores,
            callback=validate_gitignores,
            is_eager=True,
        ),
    ],
    path: Annotated[
        Path | None,
        # this is not working yet - see
        typer.Option(
            "--path",
            "-p",
            help="path to .gitignore file [default: current directory]",
            file_okay=False,
            dir_okay=True,
            exists=True,
            is_eager=True,
        ),
    ] = Path.cwd(),  # noqa: B008  # function-call-in-default-argument
    append: Annotated[
        bool | None,
        typer.Option(
            "--append",
            "-a",
            help="append to existing .gitignore file",
            show_default=True,
            is_eager=True,
        ),
    ] = False,
    overwrite: Annotated[
        bool | None,
        typer.Option(
            "--overwrite",
            "-o",
            help="overwrite existing .gitignore file",
            show_default=True,
            is_eager=True,
        ),
    ] = False,
    prettier: Annotated[
        bool | None,
        typer.Option(
            "--prettier",
            "-r",
            help="save as .prettierignore",
            show_default=True,
            is_eager=True,
        ),
    ] = False,
    list_gitignores: Annotated[
        bool | None,
        typer.Option(
            "--list",
            "-l",
            help="list available languages/frameworks for .gitignore",
            is_eager=True,
            callback=list_gitignores,
        ),
    ] = False,
) -> None:
    """
    Create a .gitignore (or .prettierignore with --prettier) file for over 500 languages and frameworks.
    Currently, the source for the ignore files is https://gitignore.io but this may change in the future
    to ensure the most up-to-date ignore files are used (see also https://github.com/toptal/gitignore.io/issues/650).
    """
    # Consider using https://donotcommit.com/api as a source instead of gitignore.io once they expand available languages
    typer.completion.completion_init()
    if append and overwrite:
        raise typer.BadParameter(
            "Cannot use both append and overwrite options at the same time.",
            param_hint=["append", "overwrite"],
        )
    if path.is_dir():
        if prettier:
            path = path / ".prettierignore"
        else:
            path = path / ".gitignore"
    else:
        # this should be caught by the file_okay=False option
        raise typer.BadParameter(
            "Path must be a directory. Please provide a directory path to create the .gitignore file."
        )
    if path.exists():
        if not append and not overwrite:
            a_o_c = Prompt.ask(
                f"{path} already exists. Do you want to overwrite, append, or cancel? (o/a/c)",
            )
            if a_o_c == "a":
                append = True
                overwrite = False
            elif a_o_c == "o":
                append = False
                overwrite = True
            else:
                raise typer.Abort()
        if append and not overwrite:
            with open(path, "a+") as f:
                f.write(f"\n\n{get_gitignore(languages)}")
            rprint(
                f"[green]Appended {get_file_type_links(languages)} {'prettierignore' if prettier else 'gitignore'} to existing file at {path}[/green]"
            )
        elif overwrite and not append:
            with open(path, "w") as f:
                f.write(get_gitignore(languages))
            rprint(
                f"[green]Overwrote existing file with {get_file_type_links(languages)} {'prettierignore' if prettier else 'gitignore'} at {path}[/green]"
            )
        else:
            # this should be caught by the append and overwrite check above
            raise typer.BadParameter(
                "Cannot use both append and overwrite options at the same time.",
                param_hint=["append", "overwrite"],
            )
    else:
        with open(path, "w") as f:
            f.write(get_gitignore(languages))
        rprint(
            f"[green]Created {get_file_type_links(languages)} {'prettierignore' if prettier else 'gitignore'} at {path}[/green]"
        )
    typer.Exit(code=0)


if __name__ == "__main__":
    app()
