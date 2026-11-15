"""Pre-commit hook for validating Chezmoi Zsh templates or Zsh scripts."""

import subprocess # nosec B404: required to execute chezmoi and zsh.
import sys
from pathlib import Path


SUPPORTED_PREFIX = (
    "dot_zshrc",
    "dot_zshenv",
    "dot_zprofile",
    "dot_zlogin",
    "dot_zlogout",
    "run_"
)
TEMPLATE_SUFFIX = ".tmpl"
CHEZMOI_COMMAND_RENDER = ["chezmoi", "execute-template"]
ZSH_SYNTAX_CHECK = ["zsh", "-n"]


def _has_supported_prefix(file_name: str) -> bool:
    """Check if `file_name` starts with a supported `chezmoi` prefix.

    Args
    ----
        file_name (str): file name (without directories) to check.

    Returns
    -------
        bool
            True if `file_name` starts with on of `SUPPORTED_PREFIX`; otherwise False."""
    return file_name.startswith(SUPPORTED_PREFIX)

def is_template(path: str) -> bool:
    """Check if the file name in `path` is a `chezmoi` template to be rendered before
    validating syntax.

    Args
    ----
        path (str): path of the file to check.

    Returns
    -------
        bool
            True if `path` file name is a template to render; otherwise False.
    """
    name = Path(path).name
    return name.endswith(TEMPLATE_SUFFIX) and _has_supported_prefix(name)

def is_script(path: str) -> bool:
    """Check if the file name in `path` is a shell script to validate syntax.

    Args
    ----
        path (str): path of the file to check.

    Returns
    -------
        bool
            True if `path` file name is a shell script; otherwise False.
    """
    name = Path(path).name
    return not name.endswith(TEMPLATE_SUFFIX) and (
        _has_supported_prefix(name) or name.endswith((".sh", ".zsh"))
    )

def validate_zsh_syntax(path: str) -> bool:
    """Check if file name in `path` has a valid `zsh` syntax.

    Templates are rendered with `chezmoi` first, then the output is validated.
    A template that fails to render is considered invalid.

    Args
    ----
        path (str): path of the file to check.

    Returns
    -------
        bool
            True if `path` file name has a valid `zsh` syntax; otherwise False.
    """
    with Path(path).open("rb") as file:
        if is_template(path):
            rendered = subprocess.run(
                CHEZMOI_COMMAND_RENDER, stdin=file, capture_output=True, check=False
            ) # nosec B603: arguments are passed without a shell.
            if rendered.returncode != 0:
                return False
            source = rendered.stdout
        else:
            source = file.read()

    result = subprocess.run(
        ZSH_SYNTAX_CHECK, input=source, capture_output=True, check=False
    ) # nosec B603: arguments are passed without a shell.
    return result.returncode == 0

def main() -> int:
    """Validate shell scripts and templates received from pre-commit.

    Prints `PASS` or `FAIL` for each validated file; files that are neither templates nor scripts
    are skipped.

    Returns
    -------
        int
            1 if validation fails otherwise 0.
    """
    failed = False
    for p in sys.argv[1:]:
        if not is_template(p) and not is_script(p):
            continue
        if validate_zsh_syntax(p):
            print(f"PASS: {p}")
        else:
            print(f"FAIL: {p}")
            failed = True
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
