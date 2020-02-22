"""
Main invocation for spelling check
"""
from __future__ import absolute_import, division, print_function

import pathlib

import pyspelling

from spelling.config import get_config_context_manager
from spelling.store import get_store


def check(display_context, display_summary, config, storage_path, fobj):
    """
    Execute the invocation
    """
    workingpath = pathlib.Path(".").resolve()
    success = True
    check_iter_output = check_iter(
        display_context, display_summary, config, storage_path, workingpath
    )
    for output in check_iter_output:
        print(output, file=fobj)
        success = False
    if success:
        print("Spelling check passed :)", file=fobj)
    return success


def check_iter(display_context, display_summary, config, storage_path, workingpath):
    """
    Execute the invocation
    """
    all_results = run_spell_check(config, storage_path, workingpath)
    yield from process_results(all_results, display_context, display_summary)


def process_results(all_results, display_context, display_summary):
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


def run_spell_check(config, storage_path, workingpath):
    """
    Perform the spell check and keep a record of spelling mistakes.
    """
    with get_config_context_manager(workingpath, config) as ctxt:
        all_results = list(
            pyspelling.spellcheck(
                ctxt.config,
                names=[],
                groups=[],
                binary="",
                sources=[],
                verbose=0,
                debug=False,
            )
        )
    storage = get_store(storage_path)
    wordcount = storage.load_word_count()
    for results in all_results:
        for word in results.words:
            wordcount[word] = wordcount.get(word, 0) + 1
    storage.save_word_count(wordcount)
    return all_results


# vim: set ft=python:
