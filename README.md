# prekmoi

| Category      | Badges |
| :---          | :---   |
| License       | [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) |
| PyPI          | [![PyPI](https://img.shields.io/pypi/v/prekmoi)](https://pypi.org/project/prekmoi/) |
| Docs          | [![Documentation](https://img.shields.io/badge/docs-online-blue.svg)](https://baldoefiero.github.io/prekmoi/)

| Build         | Status |
| :---          | :---   |
| Quality       | [![CI - Quality](https://github.com/baldoefiero/prekmoi/actions/workflows/quality.yml/badge.svg)](https://github.com/baldoefiero/prekmoi/actions/workflows/quality.yml) |
| Documentation | [![CI - Docs](https://github.com/baldoefiero/prekmoi/actions/workflows/docs.yml/badge.svg)](https://github.com/baldoefiero/prekmoi/actions/workflows/docs.yml) |
| Publish       | [![CI - Publish](https://github.com/baldoefiero/prekmoi/actions/workflows/publish.yml/badge.svg)](https://github.com/baldoefiero/prekmoi/actions/workflows/publish.yml) |

**prekmoi** is a [prek](https://prek.j178.dev/) hook that validates the Zsh syntax in
[Chezmoi](https://chezmoi.io) templates and standalone Zsh scripts.

It automatically selects supported files, renders Chezmoi templates when necessary, and checks the
resulting Zsh syntax without executing the scripts.

**Contents**

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How It Works](#how-it-works)
- [Bug Reports](#bug-reports)
- [License](#license)

## Features

- Validates Chezmoi Zsh templates after rendering.
- Validates standalone Zsh scripts without rendering.
- Uses `chezmoi execute-template` for template rendering.
- Uses `zsh -n` for syntax validation.
- Skips unsupported files automatically through `prek`.
- Does not execute validated scripts.

## Requirements

- Python 3.11+
- [zsh](https://www.zsh.org/)
- [Chezmoi](https://chezmoi.io)
- [prek](https://prek.j178.dev/)

## Installation

Add the following to your `.pre-commit-config.yaml` file.

```yaml
repos:
  - repo: https://github.com/baldoefiero/prekmoi
    rev: v0.1.0
    hooks:
      - id: prekmoi
```

## How It Works

prekmoi uses `prek` to select files based on their paths and names.

**Chezmoi templates**

Files matching a supported prefix and ending in `.tmpl` are rendered using
`chezmoi execute-template`.

The rendered output is then passed to `zsh -n` for syntax validation.

If rendering fails, the file is considered invalid and syntax validation is skipped.

**Zsh scripts**

Files selected by `prek` that do not end in `.tmpl` are passed directly to `zsh -n` without
template rendering.

**Supported prefixes**

The following filename prefixes are supported:

| Prefix       |
| :---         |
| dot_zshrc    |
| dot_zshenv   |
| dot_zprofile |
| dot_zlogin   |
| dot_zlogout  |
| run_         |

Files that do not match the selection rules are ignored by `prek`.

## Bug Reports

Found a bug or something not working as expected?

Please [open an issue](https://github.com/baldoefiero/prekmoi/issues) and include:

- A description of the problem
- Steps to reproduce it
- Relevant error messages or output
- You operating system and the versions of Python, Zsh, Chezmoi and prek.

## License

prekmoi is distributed under the [MIT License](LICENSE).
