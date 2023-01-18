#!/usr/bin/env python
"""
Module load handler for execution via:

python -m spelling
"""
from __future__ import absolute_import, division, print_function

import contextlib
import io
import logging
import os
import pathlib
import sys

import click

from spelling.check import check_iter
from spelling.dependencies import ensure_dependencies
from spelling.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
@click.option("--display-context/--no-display-context", default=True)
@click.option("--display-summary/--no-display-summary", default=True)
@click.option("--display-help/--no-display-help", default=True)
@click.option("--config", default=None)
@click.option("--use-unanimous/--no-unanimous", default=True)
@click.option("--working-path", default=None)
@click.option("--json-path", default=None)
def main(  # pylint: disable=too-many-arguments
    ctxt,
    display_context,
    display_summary,
    display_help,
    config,
    use_unanimous,
    working_path,
    json_path,
):
    """
    Used to conveniently invoke spell checking with sensible defaults and
    command line arguments to change the behavior.
    """
    if ctxt.invoked_subcommand is None:
        run_invocation(
            display_context,
            display_summary,
            display_help,
            config,
            use_unanimous,
            working_path,
            json_path,
        )


@main.command()
@click.option("--display-context/--no-display-context", default=True)
@click.option("--display-summary/--no-display-summary", default=True)
@click.option("--display-help/--no-display-help", default=True)
@click.option("--config", default=None)
@click.option("--use-unanimous/--no-unanimous", default=True)
@click.option("--working-path", default=None)
@click.option("--json-path", default=None)
def invoke(  # pylint: disable=too-many-arguments
    display_context,
    display_summary,
    display_help,
    config,
    use_unanimous,
    working_path,
    json_path,
):
    """
    Invoke the spell checker
    """
    run_invocation(
        display_context,
        display_summary,
        display_help,
        config,
        use_unanimous,
        working_path,
        json_path,
    )


@contextlib.contextmanager
def wrap_open(path):
    """
    Handle path is None otherwise open in context manager
    """
    if path is None:
        yield None
        return
    with io.open(path, "w", encoding="utf-8") as fobj:
        yield fobj


def run_invocation(  # pylint: disable=too-many-arguments
    display_context,
    display_summary,
    display_help,
    config,
    use_unanimous,
    working_path,
    json_path,
):
    """
    Call spell checker
    """
    logging.basicConfig()
    try:
        ensure_dependencies()
        success = True
        if working_path is None:
            working_path = pathlib.Path(os.getcwd()).resolve()
        with wrap_open(json_path) as jsonfobj:
            msg_iter = check_iter(
                display_context=display_context,
                display_summary=display_summary,
                display_help=display_help,
                config=config,
                use_unanimous=use_unanimous,
                workingpath=working_path,
                jsonfobj=jsonfobj,
            )
            for msg in msg_iter:
                print(msg)
                success = False
        if not success:
            sys.exit(1)
        print("Spelling check passed :)")
    except Exception:
        logging.exception("Error during processing.")
        sys.exit(2)
        raise


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
