"""
Tools to load the default `.pyspelling` config and update it with the
nonwords dictionary and the custom exclusions.
"""

import pathlib
import shutil
import tempfile
from contextlib import contextmanager


class ConfigContext(object):
    """
    Class to load the default `.pyspelling` config and update it with the
    nonwords dictionary and the custom exclusions.
    """

    def __init__(self, tmppath):
        self.tmppath = tmppath


@contextmanager
def get_config_context_manager():
    """
    Loads the default `.pyspelling` config and then updates it with the
    nonwords dictionary and the custom exclusions in a context manager that
    cleans up on completion.
    """
    tmpdir = tempfile.mkdtemp()
    yield ConfigContext(pathlib.Path(tmpdir))
    shutil.rmtree(tmpdir)
