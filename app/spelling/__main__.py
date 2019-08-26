#!/usr/bin/env python
"""
Module load handler for execution via:

python -m spelling
"""
from __future__ import absolute_import, division, print_function

import sys

import click
import pkg_resources
import pyspelling.__main__

from .version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
def main(ctxt):
    """
    Used to conveniently invoke spell checking with sensible defaults and
    command line arguments to change the behavior.
    """
    if ctxt.invoked_subcommand is None:
        run_invocation()


@main.command()
def invoke():
    """
    Invoke the spell checker
    """
    run_invocation()


def run_invocation():
    """
    Execute the invocation
    """
    configpath = pkg_resources.resource_filename(__name__, ".pyspelling.yml")
    fail = pyspelling.__main__.run(
        configpath,
        names=[],
        groups=[],
        binary="",
        spellchecker="",
        sources=[],
        verbose=0,
        debug=False,
    )

    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
