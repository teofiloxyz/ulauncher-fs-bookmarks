import os
import subprocess
from typing import List, Dict, Optional


class FSBPicker:
    def __init__(self, preferences: Dict) -> None:
        self.fs_bookmarks_path = preferences["fs_bookmarks_path"]
        self.max_search_results = int(preferences["max_search_results"])

    def fuzzy_search_fs_bookmark(self, query: str) -> Optional[List[str]]:
        cmd = f'cat "{self.fs_bookmarks_path}" | fzf --filter "{query}"'
        try:
            output = subprocess.check_output(cmd, text=True, shell=True)
        except subprocess.CalledProcessError:
            return None
        return output.splitlines()[: self.max_search_results]


class FSBFile:
    def __init__(self, preferences: Dict) -> None:
        self.fs_bookmarks_path = preferences["fs_bookmarks_path"]

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
        if not os.path.exists(self.fs_bookmarks_path):
            return []
        with open(self.fs_bookmarks_path, "r") as f:
            return [line.strip() for line in f.readlines()]

    def _write_fs_bookmarks(self, fs_bookmarks: List[str]) -> None:
        with open(self.fs_bookmarks_path, "w") as f:
            f.write("\n".join(fs_bookmarks))
