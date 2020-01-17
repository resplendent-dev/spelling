"""
Main invocation for spelling check
"""
from __future__ import absolute_import, division, print_function

import pkg_resources
import pyspelling

from spelling.store import get_store


def check(display_context, display_summary, config, storage_path, fobj):
    """
    Execute the invocation
    """
    success = True
    for output in check_iter(display_context, display_summary, config, storage_path):
        print(output, file=fobj)
        success = False
    if success:
        print("Spelling check passed :)", file=fobj)
    return success


def check_iter(display_context, display_summary, config, storage_path):
    """
    Execute the invocation
    """
    all_results = run_spell_check(config, storage_path)
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


def run_spell_check(config, storage_path):
    """
    Perform the spell check and keep a record of spelling mistakes.
    """
    if config is None:
        config = pkg_resources.resource_filename(__name__, ".pyspelling.yml")
    all_results = list(
        pyspelling.spellcheck(
            config, names=[], groups=[], binary="", sources=[], verbose=0, debug=False
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
