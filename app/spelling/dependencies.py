"""
Make sure aspell is installed.
"""

import subprocess  # noqa=S404
import sys

import distro
from whichcraft import which

HANDLERS = {
    "debian": [
        ["sudo", "--non-interactive", "apt-get", "update"],
        [
            "sudo",
            "--non-interactive",
            "apt-get",
            "install",
            "-y",
            "aspell",
            "aspell-en",
        ],
    ],
    "arch": [
        [
            "sudo",
            "--non-interactive",
            "pacman",
            "-S",
            "aspell",
            "aspell-en",
        ],
    ],
    "rhel": [
        [
            "sudo",
            "--non-interactive",
            "yum",
            "install",
            "epel-release",
        ],
        [
            "sudo",
            "--non-interactive",
            "yum",
            "install",
            "aspell",
            "aspell-en",
        ],
    ],
    "fedora": [
        [
            "sudo",
            "--non-interactive",
            "dnf",
            "install",
            "aspell",
            "aspell-en",
        ],
    ]
}


def ensure_dependencies():
    """
    Check for presence of aspell
    """
    if which("aspell") is not None:
        return
    distro_id = distro.id()
    distro_like = distro.like()
    try:
        try:
            handler = HANDLERS[distro_id]
        except KeyError:
            handler = HANDLERS[distro_like]
    except KeyError:
        print(
            f"Unsupported Distribution: {distro_id} please add me to "
            f"https://github.com/resplendent-dev/spelling/blob/master"
            f"/app/spelling/dependencies.py",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        for cmdargs in handler:
            subprocess.call(cmdargs)  # noqa=S603


if __name__ == "__main__":
    ensure_dependencies()
