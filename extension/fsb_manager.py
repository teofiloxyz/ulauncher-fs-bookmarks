import os
import subprocess
import sys
from typing import List, Dict, Optional

EXT_PATH = os.path.dirname(sys.argv[0])
FSB_PATH = os.path.join(EXT_PATH, "fs_bookmarks")


class FSBPicker:
    def __init__(self, preferences: Dict) -> None:
        self.max_search_results = int(preferences["max_search_results"])

    def fuzzy_search_fs_bookmark(self, query: str) -> Optional[List[str]]:
        cmd = f'cat "{FSB_PATH}" | fzf --filter "{query}"'
        try:
            output = subprocess.check_output(cmd, text=True, shell=True)
        except subprocess.CalledProcessError:
            return None
        return output.splitlines()[: self.max_search_results]


class FSBFile:
    def add_fs_bookmark(self, fs_bookmark: str) -> None:
        fs_bookmarks = self.read_fs_bookmarks()
        fs_bookmarks.append(fs_bookmark)
        fs_bookmarks.sort()
        self._write_fs_bookmarks(fs_bookmarks)

    def remove_fs_bookmark(self, fs_bookmark: str) -> None:
        fs_bookmarks = self.read_fs_bookmarks()
        fs_bookmarks.remove(fs_bookmark)
        self._write_fs_bookmarks(fs_bookmarks)

    def read_fs_bookmarks(self) -> List[str]:
        if not os.path.exists(FSB_PATH):
            return []
        with open(FSB_PATH, "r") as f:
            return [line.strip() for line in f.readlines()]

    def _write_fs_bookmarks(self, fs_bookmarks: List[str]) -> None:
        with open(FSB_PATH, "w") as f:
            f.write("\n".join(fs_bookmarks))
