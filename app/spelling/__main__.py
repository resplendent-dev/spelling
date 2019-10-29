#!/usr/bin/env python
"""
Module load handler for execution via:

python -m spelling
"""
from __future__ import absolute_import, division, print_function

import sys

import click
import pkg_resources
import pyspelling

from .version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
@click.option("--display-context/--no-display-context", default=False)
def main(ctxt, display_context):
    """
    Used to conveniently invoke spell checking with sensible defaults and
    command line arguments to change the behavior.
    """
    if ctxt.invoked_subcommand is None:
        run_invocation(display_context)


@main.command()
@click.option("--display-context/--no-display-context", default=False)
def invoke(display_context):
    """
    Invoke the spell checker
    """
    run_invocation(display_context)


def run_invocation(display_context):
    """
    Execute the invocation
    """
    configpath = pkg_resources.resource_filename(__name__, ".pyspelling.yml")
    all_results = pyspelling.spellcheck(
        configpath, names=[], groups=[], binary="", sources=[], verbose=0, debug=False
    )
    fail = False
    misspelt = set()
    for results in all_results:
        if results.error:
            fail = True
            print("ERROR: %s -- %s" % (results.context, results.error))
        elif results.words:
            fail = True
            misspelt.update(results.words)
            if display_context:
                print(
                    "Misspelled words:\n<%s> %s" % (results.category, results.context)
                )
                print("-" * 80)
                for word in results.words:
                    print(word)
                print("-" * 80)
                print("")

    if fail:
        print("!!!Spelling check failed!!!")
        if not display_context:
            print("\n".join(sorted(misspelt)))
        sys.exit(1)
    else:
        print("Spelling check passed :)")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
