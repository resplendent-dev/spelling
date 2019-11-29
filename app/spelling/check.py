"""
Main invocation for spelling check
"""
from __future__ import absolute_import, division, print_function

import pkg_resources
import pyspelling


def check(display_context, display_summary, config, fobj):
    """
    Execute the invocation
    """
    success = True
    for output in check_iter(display_context, display_summary, config):
        print(output, file=fobj)
        success = False
    if success:
        print("Spelling check passed :)", file=fobj)
    return success


def check_iter(display_context, display_summary, config):
    """
    Execute the invocation
    """
    if config is None:
        config = pkg_resources.resource_filename(__name__, ".pyspelling.yml")
    all_results = pyspelling.spellcheck(
        config, names=[], groups=[], binary="", sources=[], verbose=0, debug=False
    )
    fail = False
    misspelt = set()
    for results in all_results:
        if results.error:
            fail = True
            print("ERROR: %s -- %s" % (results.context, results.error), file=fobj)
        elif results.words:
            fail = True
            misspelt.update(results.words)
            if display_context:
                print(
                    "Misspelled words:\n<%s> %s" % (results.category, results.context),
                    file=fobj,
                )
                print("-" * 80, file=fobj)
                for word in results.words:
                    print(word, file=fobj)
                print("-" * 80, file=fobj)
                print("", file=fobj)

    if fail:
        yield "!!!Spelling check failed!!!"
        if display_summary:
            yield "\n".join(sorted(misspelt))


# vim: set ft=python:
