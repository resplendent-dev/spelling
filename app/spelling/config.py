"""
Tools to load the default `.pyspelling` config and update it with the
nonwords dictionary and the custom exclusions.
"""

import io
import pathlib
import shutil
import tempfile
from contextlib import contextmanager

import pkg_resources
import yaml
from unanimous.store import get_current_non_words


class ConfigContext(object):
    """
    Class to load the default `.pyspelling` config and update it with the
    nonwords dictionary and the custom exclusions.
    """

    def __init__(self, tmppath, config):
        self.tmppath = tmppath
        self.origconfig = config
        self.config = tmppath / ".pyspelling"
        self.wordlist = tmppath / "wordlist.txt"
        self.init()

    @staticmethod
    def load(config=None):
        """
        Open the existing config
        """
        if config is None:
            config = pkg_resources.resource_filename(__name__, ".pyspelling.yml")
        with io.open(config, "r", encoding="utf-8") as fobj:
            return yaml.safe_load(fobj)

    @staticmethod
    def save(target, yamldata):
        """
        Save the updated config
        """
        yaml.safe_dump(target, yamldata)

    def init(self):
        """
        Prepare the updated config
        """
        data = self.load(self.origconfig)
        nonwords = get_current_non_words()
        with io.open(self.wordlist, "w", encoding="utf-8") as fobj:
            for nonword in nonwords:
                print(nonword, file=fobj)
        self.update(data)
        with io.open(self.config, "w", encoding="utf-8") as fobj:
            self.save(data, fobj)

    def update(self, data):
        """
        Reconfigure the loaded yaml data as required
        """
        wordlists = [str(self.wordlist)]
        for entry in data["matrix"]:
            entry["dictionary"].setdefault("wordlists", []).extend(wordlists)


@contextmanager
def get_config_context_manager(config=None):
    """
    Loads the default `.pyspelling` config or the one provided and then
    updates it with the nonwords dictionary and the custom exclusions in a
    context manager that cleans up on completion.
    """
    tmpdir = tempfile.mkdtemp()
    yield ConfigContext(pathlib.Path(tmpdir), config)
    shutil.rmtree(tmpdir)
