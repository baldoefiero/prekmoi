# prekmoi

<!-- markdownlint-disable MD013 -->
| Category      | Badges                                                                                                        |
| :---          | :---                                                                                                          |
| License       | [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)                                     |
| PyPI          | [![PyPI](https://img.shields.io/pypi/v/prekmoi)](https://pypi.org/project/prekmoi/)                           |
| Docs          | [![Documentation](https://img.shields.io/badge/docs-online-blue.svg)](https://baldoefiero.github.io/prekmoi/) |

| Build         | Status                                                                                                                                                                  |
| :---          | :---                                                                                                                                                                    |
| Quality       | [![CI - Quality](https://github.com/baldoefiero/prekmoi/actions/workflows/quality.yml/badge.svg)](https://github.com/baldoefiero/prekmoi/actions/workflows/quality.yml) |
| Documentation | [![CI - Docs](https://github.com/baldoefiero/prekmoi/actions/workflows/docs.yml/badge.svg)](https://github.com/baldoefiero/prekmoi/actions/workflows/docs.yml)          |
| Publish       | [![CI - Publish](https://github.com/baldoefiero/prekmoi/actions/workflows/publish.yml/badge.svg)](https://github.com/baldoefiero/prekmoi/actions/workflows/publish.yml) |
<!-- markdownlint-enable -->

**prekmoi** is a [prek](https://prek.j178.dev/) hook that validates the Zsh
syntax in [Chezmoi](https://chezmoi.io) templates and standalone Zsh scripts.

It automatically selects supported files, renders Chezmoi templates when
necessary, and checks the resulting Zsh syntax without executing the scripts.

<!-- markdownlint-disable MD036 -->
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of contents**

- [Documentation](#documentation)
- [Bug Reports](#bug-reports)
- [License](#license)

<!-- END doctoc -->
<!-- markdownlint-enable -->

## Documentation

Check the [official documentation](https://baldoefiero.github.io/prekmoi/) to
know how to setup and use **prekmoi**.

## Bug Reports

Found a bug or something not working as expected?

Please [open an issue](https://github.com/baldoefiero/prekmoi/issues) and
include:

- A description of the problem
- Steps to reproduce it
- Relevant error messages or output
- You operating system and the versions of Python, Zsh, Chezmoi and prek.

## License

prekmoi is distributed under the [MIT License](LICENSE).
