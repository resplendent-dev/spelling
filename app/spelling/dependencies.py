"""
Make sure aspell is installed.
"""

import os
import subprocess  # noqa=S404 # nosec
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
    "arch": [["sudo", "--non-interactive", "pacman", "-S", "aspell", "aspell-en"]],
    "rhel": [
        ["sudo", "--non-interactive", "yum", "install", "epel-release"],
        ["sudo", "--non-interactive", "yum", "install", "aspell", "aspell-en"],
    ],
    "fedora": [["sudo", "--non-interactive", "dnf", "install", "aspell", "aspell-en"]],
}

CI_ENVS = {
    "CI",
    "APPVEYOR",
    "TF_BUILD",
    "CIRCLECI",
    "CI_SERVER",
    "GITLAB_CI",
    "CONTINUOUS_INTEGRATION",
    "TRAVIS",
    "IS_CI",
    "IN_CI",
}


def ensure_dependencies():
    """
    Check for presence of aspell
    """
    if which("aspell") is not None:
        return
    if not is_in_ci():
        print(
            "aspell and aspell-en need to be installed. "
            " Environment does not appear to be inside a"
            " CI system so timidly refusing to continue.",
            file=sys.stderr,
        )
        sys.exit(1)
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
            subprocess.call(cmdargs)  # noqa=S603 # nosec


def is_in_ci():
    """
    Check common CI environment variables
    """
    return bool(CI_ENVS.intersection(os.environ.keys()))


if __name__ == "__main__":
    ensure_dependencies()
