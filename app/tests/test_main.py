"""
Test modules for spelling.__main__
"""


import pytest
from click.testing import CliRunner
from spelling.__main__ import main

from .util import get_tmpdir


@pytest.mark.parametrize(
    "args,", [(), ("--display-context",), ("--no-display-context",)]
)
def test_main_emptydir(args):
    """
    GIVEN an empty directory WHEN calling main THEN the call executes
    successfully with a exit_code of 0 and a success message
    """
    # Setup
    runner = CliRunner()
    with get_tmpdir():
        # Exercise
        result = runner.invoke(main, args)
    # Verify
    assert result.output.strip() == "Spelling check passed :)"  # nosec
    assert result.exit_code == 0  # nosec
