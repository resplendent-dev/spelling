"""
Test modules for spelling.__main__
"""


from click.testing import CliRunner


def test_main_emptydir():
    """
    GIVEN an empty directory WHEN calling main THEN the call executes
    successfully with a exit_code of 0 and a success message
    """
    # Setup
    from spelling.__main__ import main
    from .util import get_tmpdir

    runner = CliRunner()
    with get_tmpdir():
        # Exercise
        result = runner.invoke(main, [])
    # Verify
    assert result.output == 'Spelling check passed :)\n'  # nosec
    assert result.exit_code == 0  # nosec
