from enum import Enum, auto
import os

from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.ExtensionCustomAction import (
    ExtensionCustomAction,
)
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class Icon:
    default = "images/icon.png"
    folder = "images/folder_bookmark.png"
    file = "images/file_bookmark.png"


class CustomActionOption(Enum):
    ADD_FSB = auto()
    REM_FSB = auto()


class ResultItemGenerator:
    def generate_item_to_open(
        self, fs_bookmark: str, cmd_on_enter: str, cmd_on_alt_enter: str
    ) -> ExtensionResultItem:
        return ExtensionResultItem(
            name=fs_bookmark,
            icon=self._get_icon_from_path(fs_bookmark),
            on_enter=RunScriptAction(
                self._put_fs_bookmark_on_cmd(cmd_on_enter, fs_bookmark)
            ),
            on_alt_enter=RunScriptAction(
                self._put_fs_bookmark_on_cmd(cmd_on_alt_enter, fs_bookmark)
            ),
        )

    def generate_item_to_add(self, query: str) -> ExtensionResultItem:
        return ExtensionResultItem(
            name=query,
            icon=self._get_icon_from_path(query),
            description="Add New FS Bookmark?",
            on_enter=ExtensionCustomAction(
                (CustomActionOption.ADD_FSB, query), keep_app_open=False
            ),
        )

    def generate_item_to_remove(
        self,
        fs_bookmark: str,
    ) -> ExtensionResultItem:
        return ExtensionResultItem(
            name=fs_bookmark,
            icon=self._get_icon_from_path(fs_bookmark),
            description="Remove FS Bookmark?",
            on_enter=ExtensionCustomAction(
                (CustomActionOption.REM_FSB, fs_bookmark), keep_app_open=False
            ),
        )

    @staticmethod
    def generate_message_item(
        title: str, description: str = ""
    ) -> ExtensionResultItem:
        return ExtensionResultItem(
            name=title,
            icon=Icon.default,
            description=description,
            on_enter=DoNothingAction(),
        )

    @staticmethod
    def generate_hide_item() -> ExtensionResultItem:
        return ExtensionResultItem(
            on_enter=HideWindowAction(),
        )

    @staticmethod
    def _get_icon_from_path(path: str) -> str:
        if not os.path.exists(path):
            return Icon.default
        if os.path.isdir(path):
            return Icon.folder
        return Icon.file

    @staticmethod
    def _put_fs_bookmark_on_cmd(cmd: str, fs_bookmark: str) -> str:
        return cmd.replace("%fs_bookmark%", f'"{fs_bookmark}"')
