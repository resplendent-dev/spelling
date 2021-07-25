"""
Test modules for spelling.__main__
"""


import io
import os
import pathlib
import sys
import zipfile

import pytest
from click.testing import CliRunner

from spelling.__main__ import main

from .util import get_tmpdir

BADDATA = {"test.rst": "boguz\n"}
BADMARKDOWN = {
    "test.md": """
# test

some bad wordishes that are short like jk.

are thuj word found.
""",
    "CHANGELOG.md": """
#  test

spellingish errars should be ignored here.
""",
}
BADCONFIG = """
spellchecker: aspell

matrix:
- name: restructedtext
  expect_match: false
  sources:
  -
    - "**/*.rst"
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
  -
    - "**/*.rst"
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


def get_test_data_path():
    """
    Locate the directory of the root folder for the project
    """
    this_file = pathlib.Path(sys.modules[__name__].__file__).resolve()
    test_dir = this_file.parent
    app_dir = test_dir.parent
    return app_dir / "data" / "test" / "main"


@pytest.mark.parametrize(
    "args,filedata,expected_result,expected_exit_code,config",
    [
        ([], {}, "Spelling check passed :)", 0, None),
        (
            ["--no-display-help"],
            BADDATA,
            "ERROR: test.rst -- Failure during filtering\n"
            "!!!Spelling check failed!!!",
            1,
            BADCONFIG,
        ),
        (
            ["--no-display-help"],
            BADDATA,
            "ERROR: test.rst -- Failure during filtering\n"
            "!!!Spelling check failed!!!",
            1,
            BADCONFIGFILTER,
        ),
        (["invoke"], {}, "Spelling check passed :)", 0, None),
        (["--display-context"], {}, "Spelling check passed :)", 0, None),
        (["--no-display-context"], {}, "Spelling check passed :)", 0, None),
        (
            ["--no-display-help", "--no-display-context", "--display-summary"],
            BADDATA,
            "!!!Spelling check failed!!!\nboguz",
            1,
            None,
        ),
        (
            ["--no-display-help", "--display-context", "--no-display-summary"],
            BADDATA,
            "Misspelled words:\n"
            "<text> ${DIR}/test.rst: html>body>div>p\n"
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
            [],
            BADMARKDOWN,
            "Misspelled words:\n"
            "<text> ${DIR}/test.md: html>body>p\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "wordishes\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "\n"
            "Misspelled words:\n"
            "<text> ${DIR}/test.md: html>body>p\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "thuj\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "\n!!!Spelling check failed!!!\n"
            "thuj\n"
            "wordishes\n\n"
            "If the spelling checker reports a spelling"
            " mistake which is actually a\n"
            "deliberate choice an exemption can be made"
            " in a few ways:\n\n"
            "* Words containing uppercase characters are"
            " assumed to be proper nouns and\n"
            "  ignored.\n"
            "* Escaping can be achieved through the use"
            " of back ticks ` around the word.\n"
            "* Adding to a custom wordlist wordlist.txt"
            " or spelling_wordlist.txt found in any\n"
            "  sub-directory.\n"
            "* Adding to the global wordlist"
            " https://github.com/resplendent-dev/unanimous",
            1,
            None,
        ),
    ],
)
def test_main_data(args, filedata, expected_result, expected_exit_code, config):
    """
    GIVEN a directory with provided data WHEN calling main THEN the call
    executes with the provided exit_code and provided message
    """
    # Setup
    runner = CliRunner()
    with get_tmpdir() as path:
        expected_result = expected_result.replace("${DIR}", str(path))
        for filename, content in filedata.items():
            filepath = os.path.join(path, filename)
            with io.open(filepath, "w", encoding="utf-8") as fobj:
                print(content, file=fobj)
        if config is not None:
            configpath = os.path.join(path, ".pyspelling.yml")
            with io.open(configpath, "w", encoding="utf-8") as fobj:
                print(config, file=fobj)
            args.extend(["--config", configpath])
        os.chdir(path)
        # Exercise
        result = runner.invoke(main, args, catch_exceptions=False)
    # Verify
    assert result.output.strip() == expected_result  # nosec # noqa=S101
    assert result.exit_code == expected_exit_code  # nosec # noqa=S101


@pytest.mark.parametrize("path", list(get_test_data_path().iterdir()))
def test_main_repo_data(path, record):
    """
    GIVEN a directory with provided data WHEN calling main THEN the call
    executes with the provided exit_code and provided message
    """
    # Setup
    args = []
    runner = CliRunner()
    with get_tmpdir() as extractpath:
        expected_result_path = path / "expected_result.txt"
        if not record or expected_result_path.exists():
            with io.open(str(expected_result_path), "r", encoding="utf-8") as fobj:
                expected_result = fobj.read().strip()
                expected_result = expected_result.replace("${DIR}", str(extractpath))
        else:
            expected_result = None
        expected_exit_code_path = path / "expected_exit_code.txt"
        if not record or expected_exit_code_path.exists():
            with io.open(str(expected_exit_code_path), "r", encoding="utf-8") as fobj:
                expected_exit_code = int(fobj.read())
        else:
            expected_exit_code = None
        with zipfile.ZipFile(str(path / "data.zip")) as zipobj:
            zipobj.extractall(extractpath)
            # Exercise
            result = runner.invoke(main, args, catch_exceptions=False)
        # Verify
        if not record or expected_result_path.exists():
            result_sorted_lines = sorted(result.output.strip().splitlines())
            expected_sorted_result = sorted(expected_result.strip().splitlines())
            assert result_sorted_lines == expected_sorted_result  # nosec # noqa=S101
        else:
            with io.open(str(expected_result_path), "w", encoding="utf-8") as fobj:
                result_output = result.output
                result_output = result_output.replace(str(extractpath), "${DIR}")
                fobj.write(result_output)
    if not record or expected_exit_code_path.exists():
        assert result.exit_code == expected_exit_code  # nosec # noqa=S101
    else:
        with io.open(str(expected_exit_code_path), "w", encoding="utf-8") as fobj:
            print(str(result.exit_code), file=fobj)
