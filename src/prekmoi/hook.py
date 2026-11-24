"""Pre-commit hook for validating Chezmoi Zsh templates or Zsh scripts."""

import subprocess  # nosec B404: required to execute chezmoi and zsh.
import sys
from pathlib import Path

TEMPLATE_SUFFIX = ".tmpl"
CHEZMOI_COMMAND_RENDER = ["chezmoi", "execute-template"]
ZSH_SYNTAX_CHECK = ["zsh", "-n"]


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
        if Path(path).suffix == TEMPLATE_SUFFIX:
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
        if validate_zsh_syntax(p):
            print(f"PASS: {p}")
        else:
            print(f"FAIL: {p}")
            failed = True
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
