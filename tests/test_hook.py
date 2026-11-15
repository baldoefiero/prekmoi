"""Tests for the prekmoi hook."""

from __future__ import annotations
import shutil
import runpy
import sys
import subprocess
from subprocess import CompletedProcess
from typing import TYPE_CHECKING, Protocol, cast
import pytest
from prekmoi.hook import is_script, is_template, main, validate_zsh_syntax


if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from typing import Any
    from pytest_mock import MockerFixture


CHEZMOI_DIR = "/home/user/.local/share/chezmoi"
VALID_ZSH = "echo hello\n"
INVALID_ZSH = "if true; then\n  echo hello\n"  # missing `fi`


class FakeChezmoi(Protocol): # pylint: disable=too-few-public-methods
    """Callable installing a fake `chezmoi` render command."""

    def __call__(self, stdout: bytes = b"", returncode: int = 0) -> None: ...


requires_zsh = pytest.mark.skipif(
    shutil.which("zsh") is None, reason="zsh is not installed"
)

# (file name, is_template, is_script)
CLASSIFICATION = [
    pytest.param("run_onchange_after_x.tmpl", True, False, id="run-template"),
    pytest.param("run_onchange_after_x.sh.tmpl", True, False, id="run-sh-template"),
    pytest.param("dot_zshrc.tmpl", True, False, id="zshrc-template"),
    pytest.param("dot_zprofile.tmpl", True, False, id="zprofile-template"),
    pytest.param("dot_zshrc", False, True, id="zshrc"),
    pytest.param("dot_zprofile", False, True, id="zprofile"),
    pytest.param("run_once_install", False, True, id="run-no-extension"),
    pytest.param("run_onchange_after_x.sh", False, True, id="run-sh"),
    pytest.param("install.sh", False, True, id="sh"),
    pytest.param("aliases.zsh", False, True, id="zsh"),
    pytest.param("dot_zshrc_tmpl", False, True, id="suffix-without-dot"),
    pytest.param("README.md", False, False, id="unrelated"),
    pytest.param("dot_gitconfig.tmpl", False, False, id="unsupported-template"),
]

VALIDITY = [
    pytest.param(VALID_ZSH, True, id="valid"),
    pytest.param(INVALID_ZSH, False, id="invalid"),
]

@pytest.fixture(name="fake_chezmoi")
def fake_chezmoi_fixture(mocker: MockerFixture) -> FakeChezmoi:
    """Fake only the chezmoi command; every other command (zsh) runs for real."""
    real_run = cast("Callable[..., CompletedProcess[bytes]]", subprocess.run)

    def install(stdout: bytes = b"", returncode: int = 0, stderr: bytes = b"") -> None:
        def run(command: list[str], **kwargs: Any) -> CompletedProcess[bytes]:
            if command[0] == "chezmoi":
                return CompletedProcess(command, returncode, stdout, stderr)
            return real_run(command, **kwargs) # pylint: disable=subprocess-run-check
        mocker.patch("prekmoi.hook.subprocess.run", side_effect=run)
    return install


@pytest.mark.parametrize(("name", "template", "script"), CLASSIFICATION)
def test_classification(name: str, template: bool, script: bool) -> None:
    """Test that a file name is classified as template, script or neither."""
    path = f"{CHEZMOI_DIR}/{name}"

    assert is_template(path) is template
    assert is_script(path) is script


@requires_zsh
@pytest.mark.parametrize(("content", "expected"), VALIDITY)
def test_validate_script(
    make_file: Callable[[str, str], Path], content: str, expected: bool
) -> None:
    """Test that a script is syntax-checked by zsh as it is."""
    path = make_file("dot_zshrc", content)
    assert validate_zsh_syntax(str(path)) is expected


@requires_zsh
@pytest.mark.parametrize(("rendered", "expected"), VALIDITY)
def test_validate_template_checks_rendered_output(
    make_file: Callable[[str, str], Path],
    fake_chezmoi: Callable[..., None],
    rendered: str,
    expected: bool,
) -> None:
    """Test that a template is syntax-checked after rendering, not before."""
    path = make_file("dot_zshrc.tmpl", "{{ .anything }}")  # source is irrelevant
    fake_chezmoi(stdout=rendered.encode())

    assert validate_zsh_syntax(str(path)) is expected


def test_validate_template_render_failure_returns_false(
    make_file: Callable[[str, str], Path],
    fake_chezmoi: Callable[..., None],
) -> None:
    """Test that a template failing to render is invalid and does not raise."""
    path = make_file("dot_zshrc.tmpl", "{{ broken")
    fake_chezmoi(returncode=1)

    assert validate_zsh_syntax(str(path)) is False


@requires_zsh
def test_main_reports_pass_and_fail(
    make_file: Callable[[str, str], Path],
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that `main` reports each validated file and skips unsupported ones."""
    good = make_file("dot_zshrc", VALID_ZSH)
    bad = make_file("dot_zprofile", INVALID_ZSH)
    ignored = make_file("README.md", "not shell")
    mocker.patch("sys.argv", ["prekmoi", str(good), str(bad), str(ignored)])

    assert main() == 1

    out = capsys.readouterr().out
    assert f"PASS: {good}" in out
    assert f"FAIL: {bad}" in out
    assert str(ignored) not in out


@requires_zsh
def test_main_exit_code_zero_when_all_valid(
    make_file: Callable[[str, str], Path], mocker: MockerFixture
) -> None:
    """Test that `main` returns 0 when every validated file is valid."""
    good = make_file("dot_zshrc", VALID_ZSH)
    mocker.patch("sys.argv", ["prekmoi", str(good)])

    assert main() == 0


def test_main_without_files_returns_zero(mocker: MockerFixture) -> None:
    """Test that `main` succeeds when pre-commit passes no files."""
    mocker.patch("sys.argv", ["prekmoi"])

    assert main() == 0


@requires_zsh
@pytest.mark.parametrize(
    ("content", "exit_code"),
    [
        pytest.param(VALID_ZSH, 0, id="valid"),
        pytest.param(INVALID_ZSH, 1, id="invalid"),
    ],
)
def test_run_as_script_exits_with_main_status(
    make_file: Callable[[str, str], Path],
    mocker: MockerFixture,
    content: str,
    exit_code: int
) -> None:
    """Test that running the module as script exists with the `main` status."""
    path = make_file("dot_zshrc", content)
    mocker.patch("sys.argv", ["prekmoi", str(path)])
    # Re-execute the module from scratch, avoiding runpy's "found in sys.modules" warning.
    mocker.patch.dict("sys.modules")
    del sys.modules["prekmoi.hook"]

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("prekmoi.hook", run_name="__main__")

    assert exc_info.value.code == exit_code
