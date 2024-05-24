"""Nox file."""

import tomllib
from importlib.metadata import version
from pathlib import Path

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv|virtualenv"

# get the supported python versions from the classifiers in pyproject.toml.
# which are automatically created using pyproject-fmt
pyp = tomllib.loads(Path("pyproject.toml").read_text())
pythons = [
    pv.rsplit(" ")[-1]
    for pv in pyp["project"]["classifiers"]
    if pv.startswith("Programming Language :: Python :: 3.")
]

pydantic_oldest = "2.5"
# keep this in sync with the pydantic dependency as defined in the pyproject.toml
pydantic_latest = version("pydantic")


@nox.session(python=pythons)
@nox.parametrize("pydantic", [pydantic_latest, pydantic_oldest])
def tests(session: nox.Session, pydantic: str) -> None:
    """Testing."""
    session.install(".[dev]")

    session.install(f"pydantic=={pydantic}")
    session.run("uv", "pip", "show", "pydantic")
    session.run("coverage", "run", "-m", "pytest")

    session.notify("coverage_report")


@nox.session
def coverage_report(session: nox.Session) -> None:
    """Coverage report."""
    session.install("coverage[toml]")
    session.run("coverage", "combine")
    session.run("coverage", "report")


@nox.session
def quality(session: nox.Session) -> None:
    """Quality checks."""
    session.install(".[dev]")

    session.run(
        "ruff", "check", "src", "tests", "noxfile.py", "--fix", "--exit-non-zero-on-fix"
    )
    session.run("pyproject-fmt", "pyproject.toml")

    session.run("mypy", "src", "noxfile.py")
