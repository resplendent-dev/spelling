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
            [],
            BADDATA,
            "ERROR: test.rst -- Failure during filtering\n"
            "!!!Spelling check failed!!!",
            1,
            BADCONFIG,
        ),
        (
            [],
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
            ["--no-display-context", "--display-summary"],
            BADDATA,
            "!!!Spelling check failed!!!\nboguz",
            1,
            None,
        ),
        (
            ["--display-context", "--no-display-summary"],
            BADDATA,
            "Misspelled words:\n"
            "<text> test.rst: html>body>div>p\n"
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
            "<text> test.md: html>body>p\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "wordishes\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "\n"
            "Misspelled words:\n"
            "<text> test.md: html>body>p\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "thuj\n"
            "--------------------------------------"
            "------------------------------------------\n"
            "\n!!!Spelling check failed!!!\n"
            "thuj\n"
            "wordishes",
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
        result = runner.invoke(main, args)
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
    datazippath = path / "data.zip"
    expected_result_path = path / "expected_result.txt"
    if not record or expected_result_path.exists():
        with io.open(str(expected_result_path), "r", encoding="utf-8") as fobj:
            expected_result = fobj.read().strip()
    else:
        expected_result = None
    expected_exit_code_path = path / "expected_exit_code.txt"
    if not record or expected_exit_code_path.exists():
        with io.open(str(expected_exit_code_path), "r", encoding="utf-8") as fobj:
            expected_exit_code = int(fobj.read())
    else:
        expected_exit_code = None
    with get_tmpdir() as extractpath:
        with zipfile.ZipFile(str(datazippath)) as zipobj:
            zipobj.extractall(extractpath)
            # Exercise
            result = runner.invoke(main, args)
    # Verify
    if not record or expected_result_path.exists():
        assert result.output.strip() == expected_result  # nosec # noqa=S101
    else:
        with io.open(str(expected_result_path), "w", encoding="utf-8") as fobj:
            fobj.write(result.output)
    if not record or expected_exit_code_path.exists():
        assert result.exit_code == expected_exit_code  # nosec # noqa=S101
    else:
        with io.open(str(expected_exit_code_path), "w", encoding="utf-8") as fobj:
            print(str(result.exit_code), file=fobj)
