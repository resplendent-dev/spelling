"""failure with processing filter."""
from __future__ import print_function

from pyspelling import filters


class FailureFilter(filters.Filter):
    """Raise error during processing."""

    def get_default_config(self):
        """Get default configuration."""
        return None

    def filter(self, source_file, encoding):  # noqa A001
        """Fail processing."""
        raise Exception("Failure during filtering")

    def sfilter(self, source):
        """Fail processing."""
        raise Exception("Failure during filtering")


def get_plugin():
    """Return the filter."""

    return FailureFilter
