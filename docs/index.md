# prekmoi

**prekmoi** is a [prek](https://prek.j178.dev/) hook that validates the Zsh
syntax in [Chezmoi](https://chezmoi.io) templates and standalone Zsh scripts.

It automatically selects supported files, renders Chezmoi templates when
necessary, and checks the resulting Zsh syntax without executing the scripts.

## Features

- **Template rendering** - Uses chezmoi's native template engine with
  `chezmoi execute-template`.

- **Syntax validation** - Checks rendered scripts with `zsh -n`.

- **Rendering error reporting** - Reports template rendering failures instead
  of silently skipping validation.

- **Focused scope** - Targets Zsh templates only.

## Getting started

See the [Setup guide](setup.md) to add prekmoi to your prek configuration.
