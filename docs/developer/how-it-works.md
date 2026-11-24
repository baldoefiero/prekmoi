# How it Works

This section explains how `prekmoi` works. It uses `prek` to select files based
on their paths and names.

## Chezmoi templates

Files matching a supported prefix and ending in `.tmpl` are rendered using
`chezmoi execute-template`.

The rendered output is then passed to `zsh -n` for syntax validation.

If rendering fails, the file is considered invalid and syntax validation is
skipped.

## Zsh scripts

Files selected by `prek` that do not end in `.tmpl` are passed directly to
`zsh -n` without template rendering.

## Supported prefixes

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
