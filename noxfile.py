"""Nox file."""

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.default_venv_backend = "uv|virtualenv"

pythons = ["3.10", "3.11", "3.12"]


@nox.session(python=pythons)
def tests(session: nox.Session) -> None:
    """Testing."""
    session.install(".[dev]")
    session.run("pytest")


@nox.session()
def quality(session: nox.Session) -> None:
    """Quality checks."""
    session.install(".[dev]")

    session.run(
        "ruff", "check", "src", "tests", "noxfile.py", "--fix", "--exit-non-zero-on-fix"
    )
    session.run("mypy", "src", "noxfile.py")
