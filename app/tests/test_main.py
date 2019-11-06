"""
Test modules for spelling.__main__
"""


from click.testing import CliRunner
from spelling.__main__ import main

from .util import get_tmpdir


def test_main_emptydir():
    """
    GIVEN an empty directory WHEN calling main THEN the call executes
    successfully with a exit_code of 0 and a success message
    """
    # Setup
    runner = CliRunner()
    with get_tmpdir():
        # Exercise
        result = runner.invoke(main, [])
    # Verify
    assert result.output.strip() == "Spelling check passed :)"  # nosec
    assert result.exit_code == 0  # nosec
