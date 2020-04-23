"""
Main invocation for spelling check
"""
from __future__ import absolute_import, division, print_function

import json
import os
import pathlib

import pyspelling

from spelling.config import get_config_context_manager


def check(  # pylint: disable=too-many-arguments
    display_context, display_summary, display_help, config, fobj, jsonfobj=None
):
    """
    Execute the invocation
    """
    workingpath = pathlib.Path(".").resolve()
    success = True
    check_iter_output = check_iter(
        display_context,
        display_summary,
        display_help,
        config,
        workingpath,
        jsonfobj=jsonfobj,
    )
    for output in check_iter_output:
        print(output, file=fobj)
        success = False
    if success:
        print("Spelling check passed :)", file=fobj)
    return success


def check_iter(  # pylint: disable=too-many-arguments
    display_context, display_summary, display_help, config, workingpath, jsonfobj=None
):
    """
    Execute the invocation
    """
    all_results, custom_wordlists = run_spell_check(config, workingpath)
    if jsonfobj is not None:
        all_results = list(all_results)
        json.dump(results_to_json(all_results), jsonfobj)
    yield from process_results(
        all_results, custom_wordlists, display_context, display_summary, display_help
    )


def results_to_json(all_results):
    """
    Save the result format in a machine processable format.
    """
    words = {}
    for results in all_results:
        if results.words:
            for word in results.words:
                filename = context_to_filename(results.context)
                words.setdefault(word, {}).setdefault("files", []).append(
                    {"category": results.category, "file": filename}
                )
    return words


def context_to_filename(name):
    """
    Turn a context line into the filepath.
    """
    testname = name
    if os.path.isfile(testname):
        return testname
    testname = testname.split(":", 1)[0]
    if os.path.isfile(testname):
        return testname
    testname = testname.rsplit("(", 1)[0]
    if os.path.isfile(testname):
        return testname
    testname = testname.strip()
    if os.path.isfile(testname):
        return testname
    raise Exception(f"Unable to get filepath for {name}")


def process_results(
    all_results, custom_wordlists, display_context, display_summary, display_help
):
    """
    Work through the results yielding the words in a human readable
    output.
    """
    fail = False
    misspelt = set()
    for results in all_results:
        if results.error:
            fail = True
            yield "ERROR: %s -- %s" % (results.context, results.error)
        elif results.words:
            fail = True
            misspelt.update(results.words)
            if display_context:
                yield "Misspelled words:\n<%s> %s" % (results.category, results.context)
                yield "-" * 80
                for word in results.words:
                    yield word
                yield "-" * 80
                yield ""

    if fail:
        yield "!!!Spelling check failed!!!"
        if display_summary:
            yield "\n".join(sorted(misspelt))
        if display_help:
            yield """
If the spelling checker reports a spelling mistake which is actually a
deliberate choice an exemption can be made in a few ways:

* Words containing uppercase characters are assumed to be proper nouns and
  ignored.
* Escaping can be achieved through the use of back ticks ` around the word.
* Adding to a custom wordlist wordlist.txt or spelling_wordlist.txt found in any
  sub-directory.
* Adding to the global wordlist https://github.com/resplendent-dev/unanimous
"""
            if custom_wordlists:
                custom_wordlists_lines = "\n".join(
                    [f"* {wordlist}" for wordlist in custom_wordlists]
                )
                yield f"""
Note: The following existing custom wordlists were found in this project:
{custom_wordlists_lines}
"""


def run_spell_check(config, workingpath):
    """
    Perform the spell check and keep a record of spelling mistakes.
    """
    with get_config_context_manager(workingpath, config) as ctxt:
        all_results = list(
            pyspelling.spellcheck(
                str(ctxt.config),
                names=[],
                groups=[],
                binary="",
                sources=[],
                verbose=0,
                debug=False,
            )
        )
        return all_results, ctxt.custom_wordlists


# vim: set ft=python:
