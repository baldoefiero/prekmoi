# Setup

This section explains how to setup **prekmoi**.

## Requirements

- Python 3.11+
- [zsh](https://www.zsh.org/)
- [Chezmoi](https://chezmoi.io)
- [prek](https://prek.j178.dev/)

## Usage

Add the following to your `.pre-commit-config.yaml` file.

```yaml
repos:
  - repo: https://github.com/baldoefiero/prekmoi
    rev: v0.1.0
    hooks:
      - id: prekmoi
```
