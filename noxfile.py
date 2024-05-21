import nox

# nox.options.reuse_existing_virtualenvs = True
# nox.options.default_venv_backend = "uv|virtualenv"

pythons = ["3.10", "3.11", "3.12"]


@nox.session(python=pythons)
def tests(session: nox.Session) -> None:
    session.install(".[dev]")
    session.run("pytest")


@nox.session()
def mypy(session: nox.Session) -> None:
    session.install(".[dev]")

    session.run("mypy", "src", "noxfile.py")
