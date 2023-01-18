"""
Config tests
"""

import io
import pathlib

from spelling.config import get_config_context_manager


def test_path_update():
    """
    Ensure source path updating occurs
    """
    # Setup
    workingpath = pathlib.Path("/fake")
    # Exercise
    with get_config_context_manager(workingpath, True) as ctxt:
        # Verify
        with io.open(ctxt.config, "r", encoding="utf-8") as fobj:
            data = fobj.read()
        assert str(workingpath) in data  # nosec # noqa=S101
