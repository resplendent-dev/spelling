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


@pytest.mark.parametrize(
    "args,filedata,expected_result,expected_exit_code",
    [
        ([], {}, "Spelling check passed :)", 0),
        (["--display-context"], {}, "Spelling check passed :)", 0),
        (["--no-display-context"], {}, "Spelling check passed :)", 0),
        ([], BADDATA, "!!!Spelling check failed!!!\nboguz", 1),
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
        ),
        (["--no-display-context"], BADDATA, "!!!Spelling check failed!!!\nboguz", 1),
    ],
)
def test_main_emptydir(args, filedata, expected_result, expected_exit_code):
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
        # Exercise
        result = runner.invoke(main, args)
    # Verify
    assert result.output.strip() == expected_result  # nosec
    assert result.exit_code == expected_exit_code  # nosec
