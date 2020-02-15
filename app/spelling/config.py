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
from wcmatch import glob


class ConfigContext:
    """
    Class to load the default `.pyspelling` config and update it with the
    nonwords dictionary and the custom exclusions.
    """

    def __init__(self, tmppath, config, workingpath):
        self.tmppath = tmppath
        self.origconfig = config
        self.workingpath = workingpath
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
        for entry in data["matrix"]:
            wordlists = entry["dictionary"].get("wordlists", [])
            updated = [str(self.wordlist)]
            for wordlist in wordlists:
                wordlist = wordlist.replace("${DIR}", str(self.workingpath))
                wordlist_iglob = glob.iglob(
                    wordlist, flags=glob.N | glob.B | glob.G | glob.S | glob.O
                )
                matches = list(wordlist_iglob)
                updated.extend(matches)
            entry["dictionary"]["wordlists"] = updated
            entry["sources"] = [
                [
                    source.replace("${DIR}", str(self.workingpath))
                    for source in entry["sources"][0]
                ]
            ]


@contextmanager
def get_config_context_manager(workingpath, config=None):
    """
    Loads the default `.pyspelling` config or the one provided and then
    updates it with the nonwords dictionary and the custom exclusions in a
    context manager that cleans up on completion.
    """
    tmpdir = tempfile.mkdtemp()
    yield ConfigContext(pathlib.Path(tmpdir), config, workingpath)
    shutil.rmtree(tmpdir)
