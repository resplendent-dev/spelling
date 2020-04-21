"""
Make sure aspell is installed.
"""

import distro
from whichcraft import which


def ensure_dependencies():
    """
    Check for presence of aspell
    """
    print(distro.id())
    print(which("aspell"))


if __name__ == "__main__":
    ensure_dependencies()
