#!/usr/bin/env python
"""
Module load handler for execution via:

python -m spelling
"""
from __future__ import absolute_import, division, print_function

import io
import logging
import os
import pathlib
import sys

import click

from spelling.check import check_iter
from spelling.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
@click.option("--display-context/--no-display-context", default=True)
@click.option("--display-summary/--no-display-summary", default=True)
@click.option("--config", default=None)
@click.option("--storage-path", default=None)
@click.option("--working-path", default=None)
@click.option("--json-path", default=None)
def main(  # pylint: disable=too-many-arguments,bad-continuation
    ctxt,
    display_context,
    display_summary,
    config,
    storage_path,
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
            config,
            storage_path,
            working_path,
            json_path,
        )


@main.command()
@click.option("--display-context/--no-display-context", default=True)
@click.option("--display-summary/--no-display-summary", default=True)
@click.option("--config", default=None)
@click.option("--storage-path", default=None)
@click.option("--working-path", default=None)
@click.option("--json-path", default=None)
def invoke(  # pylint: disable=bad-continuation,too-many-arguments
    display_context, display_summary, config, storage_path, working_path, json_path
):
    """
    Invoke the spell checker
    """
    run_invocation(
        display_context, display_summary, config, storage_path, working_path, json_path
    )


def run_invocation(  # pylint: disable=bad-continuation,too-many-arguments
    display_context, display_summary, config, storage_path, working_path, json_path
):
    """
    Call spell checker
    """
    logging.basicConfig()
    try:
        success = True
        if working_path is None:
            working_path = pathlib.Path(os.getcwd()).resolve()
        jsonfobj = None
        if json_path:
            jsonfobj = io.open(json_path, "w", encoding="utf-8")
        try:
            msg_iter = check_iter(
                display_context=display_context,
                display_summary=display_summary,
                config=config,
                storage_path=storage_path,
                workingpath=working_path,
                jsonfobj=jsonfobj,
            )
            for msg in msg_iter:
                print(msg)
                success = False
        finally:
            if jsonfobj is not None:
                jsonfobj.close()
        if not success:
            sys.exit(1)
        print("Spelling check passed :)")
    except Exception:
        logging.exception("Error during processing.")
        sys.exit(2)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
