#!/usr/bin/env python
"""
Module load handler for execution via:

python -m spelling
"""
from __future__ import absolute_import, division, print_function

import sys

import click

from .check import check_iter
from .version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
@click.option("--display-context/--no-display-context", default=True)
@click.option("--display-summary/--no-display-summary", default=True)
@click.option("--config", default=None)
@click.option("--storage-path", default=None)
def main(ctxt, display_context, display_summary, config, storage_path):
    """
    Used to conveniently invoke spell checking with sensible defaults and
    command line arguments to change the behavior.
    """
    if ctxt.invoked_subcommand is None:
        run_invocation(display_context, display_summary, config, storage_path)


@main.command()
@click.option("--display-context/--no-display-context", default=True)
@click.option("--display-summary/--no-display-summary", default=True)
@click.option("--config", default=None)
@click.option("--storage-path", default=None)
def invoke(display_context, display_summary, config, storage_path):
    """
    Invoke the spell checker
    """
    run_invocation(display_context, display_summary, config, storage_path)


def run_invocation(display_context, display_summary, config, storage_path):
    """
    Call spell checker
    """
    success = True
    msg_iter = check_iter(
        display_context=display_context,
        display_summary=display_summary,
        config=config,
        storage_path=storage_path,
    )
    for msg in msg_iter:
        print(msg)
        success = False
    if not success:
        sys.exit(1)
    print("Spelling check passed :)")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
