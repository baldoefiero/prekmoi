# prekmoi

**prekmoi** is a [prek](https://prek.j178.dev/) hook that validates the Zsh syntax of rendered
[Chezmoi](https://chezmoi.io) templates.

It automatically identifies supported files, renders Chezmoi templates when necessary, and checks
their Zsh syntax without executing them.

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
- Skips unsupported files automatically.
- Does not execute validated scripts.

## Requirements

- Python 3.11+
- [zsh](https://www.zsh.org/) 5.9+
- [Chezmoi](https://chezmoi.io) 2.74.0+
- [prek](https://prek.j178.dev/) 0.5.10+

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

prekmoi identifies files based on their names and validates supported files through one of two
paths:

**Chezmoi templates**

Files with a supported prefix and a `.tmpl` suffix are rendered using `chezmoi execute-template`.
The rendered output is then passed to `zsh -n` for syntax validation.

If rendering fails, the file is considered invalid and syntax validation is skipped.

**Zsh scripts**

Files with a supported prefix or a `.sh` or `.zsh` suffix are passed directly to `zsh -n` without
template rendering.

Files that do not match either category are skipped.

Syntax validation is performed without executing the scripts.

**Supported prefixes**

| Prefix       |
| :---         |
| dot_zshrc    |
| dot_zshenv   |
| dot_zprofile |
| dot_zlogin   |
| dot_zlogout  |
| run_         |

## Bug Reports

Found a bug or something not working as expected?

Please [open an issue](https://github.com/baldoefiero/prekmoi/issues) and include:

- A description of the problem
- Steps to reproduce it
- Relevant error messages or output
- You Operating System, Python version, Zsh version, Chezmoi version and prek version.

## License

prekmoi is distributed under the [MIT License](LICENSE).
