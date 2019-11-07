"""
Test modules for spelling.__main__
"""


import io
import os

import pytest
from click.testing import CliRunner

from spelling.__main__ import main

from .util import get_tmpdir

BADDATA = {"test.rst": "boguz\n"}
BADCONFIG = """
spellchecker: aspell

matrix:
- name: restructedtext
  expect_match: false
  sources:
  - ./**/*.rst
  hunspell:
    d: en_AU
  aspell:
    lang: en
  dictionary:
    output: build/dictionary/restructured.dic
  pipeline:
  - spelling.filters.filtererr:

"""
BADCONFIGFILTER = """
spellchecker: aspell

matrix:
- name: restructedtext
  expect_match: false
  sources:
  - ./**/*.rst
  hunspell:
    d: en_AU
  aspell:
    lang: en
  dictionary:
    output: build/dictionary/restructured.dic
  pipeline:
  - unanimous.filters.nonwords:
  - spelling.filters.filtererr:

"""


@pytest.mark.parametrize(
    "args,filedata,expected_result,expected_exit_code,config",
    [
        ([], {}, "Spelling check passed :)", 0, None),
        (
            [],
            BADDATA,
            "ERROR: ./test.rst -- Failure during filtering\n"
            "!!!Spelling check failed!!!",
            1,
            BADCONFIG,
        ),
        (
            [],
            BADDATA,
            "ERROR: ./test.rst -- Failure during filtering\n"
            "!!!Spelling check failed!!!",
            1,
            BADCONFIGFILTER,
        ),
        (["invoke"], {}, "Spelling check passed :)", 0, None),
        (["--display-context"], {}, "Spelling check passed :)", 0, None),
        (["--no-display-context"], {}, "Spelling check passed :)", 0, None),
        ([], BADDATA, "!!!Spelling check failed!!!\nboguz", 1, None),
        (
            ["--display-context"],
            BADDATA,
            "Misspelled words:\n"
            "<text> ./test.rst: html>body>div>p\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "boguz\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "\n!!!Spelling check failed!!!",
            1,
            None,
        ),
        (
            ["--no-display-context"],
            BADDATA,
            "!!!Spelling check failed!!!\nboguz",
            1,
            None,
        ),
    ],
)
def test_main_emptydir(args, filedata, expected_result, expected_exit_code, config):
    """
    GIVEN an empty directory WHEN calling main THEN the call executes
    successfully with a exit_code of 0 and a success message
    """
    # Setup
    runner = CliRunner()
    with get_tmpdir() as path:
        for filename, content in filedata.items():
            filepath = os.path.join(path, filename)
            with io.open(filepath, "w", encoding="utf-8") as fobj:
                print(content, file=fobj)
        if config is not None:
            configpath = os.path.join(path, ".pyspelling.yml")
            with io.open(configpath, "w", encoding="utf-8") as fobj:
                print(config, file=fobj)
            args.extend(["--config", configpath])
        # Exercise
        result = runner.invoke(main, args)
    # Verify
    assert result.output.strip() == expected_result  # nosec
    assert result.exit_code == expected_exit_code  # nosec
