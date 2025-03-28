# `easyignore`

Create a .gitignore (or .prettierignore with --prettier) file for over 500 languages and frameworks.
Currently, the source for the ignore files is https://gitignore.io but this may change in the future
to ensure the most up-to-date ignore files are used (see also https://github.com/toptal/gitignore.io/issues/650).

**Usage**:

```console
$ easyignore [OPTIONS] LANGUAGES...
```

**Arguments**:

* `LANGUAGES...`: language/framework for .gitignore (enter as many as you like)  [required]

**Options**:

* `-p, --path DIRECTORY`: path to .gitignore file  [default: current working directory]
* `-a, --append`: append to existing .gitignore file
* `-o, --overwrite`: overwrite existing .gitignore file
* `-r, --prettier`: save as .prettierignore
* `-l, --list`: list available languages/frameworks for .gitignore
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
