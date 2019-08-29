"""
Test Utilities
"""
from __future__ import absolute_import, division, print_function

import os
import shutil
import tempfile
from contextlib import contextmanager


@contextmanager
def get_tmpdir():
    """
    Create a test directory for the current work directory
    """
    origdir = os.getcwd()
    tmpdir = tempfile.mkdtemp()
    try:
        os.chdir(tmpdir)
        yield tmpdir
    finally:
        os.chdir(origdir)
        shutil.rmtree(tmpdir, ignore_errors=True)
