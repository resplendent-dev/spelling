"""
Nox Config for running spelling
"""

import nox


@nox.session
def spelling(session):
    """
    Check spelling
    """
    session.install("spelling")
    session.run("spelling", "--version")
    session.run("flake8", "setup.py", "docs", "dummyserver", "src", "test")
    session.run("spelling")
