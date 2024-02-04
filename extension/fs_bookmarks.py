import os
from typing import Optional, Dict, List, Callable

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.RenderResultListAction import (
    RenderResultListAction,
)
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from .fsb_manager import FSBPicker, FSBFile
from .result_item_generator import ResultItemGenerator, CustomActionOption


class FSBookmarks(Extension):
    def __init__(self) -> None:
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def open_fs_bookmark(self, query: str) -> RenderResultListAction:
        if not query:
            return self._show_message("Search for a fs bookmark to open...")
        return self._render_items_based_on_search(
            query, self._render_items_to_open
        )

    def add_fs_bookmark(self, query: str) -> RenderResultListAction:
        if not query:
            return self._show_message("Add a new fs bookmark to the list...")
        elif not os.path.exists(query):
            return self._show_message("Path not recognized, cannot add this...")
        elif query in FSBFile().read_fs_bookmarks():
            return self._show_message("This path is already bookmarked...")
        return self._render_item_to_add(query)

    def remove_fs_bookmark(self, query: str) -> RenderResultListAction:
        if not query:
            return self._show_message("Search for a fs bookmark to remove...")
        return self._render_items_based_on_search(
            query, self._render_items_to_remove
        )

    def hide(self) -> RenderResultListAction:
        return RenderResultListAction(
            [ResultItemGenerator.generate_hide_item()]
        )

    def _show_message(
        self, title: str, description: str = ""
    ) -> RenderResultListAction:
        item = ResultItemGenerator.generate_message_item(title, description)
        return RenderResultListAction([item])

    def _search_fs_bookmarks(self, query: str) -> Optional[List[str]]:
        return FSBPicker(self.preferences).fuzzy_search_fs_bookmark(query)

    def _render_items_based_on_search(
        self,
        query: str,
        render_method: Callable[[List], RenderResultListAction],
    ) -> RenderResultListAction:
        results = self._search_fs_bookmarks(query)
        if not results:
            return self._show_message("No fs bookmark found...")
        return render_method(results)

    def _render_items_to_open(
        self, results: List[str]
    ) -> RenderResultListAction:
        cmd_on_enter = self.preferences["enter_action"]
        cmd_on_alt_enter = self.preferences["alt_enter_action"]
        items = [
            ResultItemGenerator().generate_item_to_open(
                fs_bookmark, cmd_on_enter, cmd_on_alt_enter
            )
            for fs_bookmark in results
        ]
        return RenderResultListAction(items)

    def _render_item_to_add(self, query: str) -> RenderResultListAction:
        item = ResultItemGenerator().generate_item_to_add(query)
        return RenderResultListAction([item])

    def _render_items_to_remove(
        self, results: List[str]
    ) -> RenderResultListAction:
        items = [
            ResultItemGenerator().generate_item_to_remove(fs_bookmark)
            for fs_bookmark in results
        ]
        return RenderResultListAction(items)


class KeywordQueryEventListener(EventListener):
    def on_event(
        self, event: KeywordQueryEvent, extension: FSBookmarks
    ) -> Optional[RenderResultListAction]:
        keyword = event.get_keyword()
        keyword_id = self._find_keyword_id(keyword, extension.preferences)
        if keyword_id == "open_fs_bookmark":
            return extension.open_fs_bookmark(event.get_argument())
        elif keyword_id == "add_fs_bookmark":
            return extension.add_fs_bookmark(event.get_argument())
        elif keyword_id == "remove_fs_bookmark":
            return extension.remove_fs_bookmark(event.get_argument())
        return None

    @staticmethod
    def _find_keyword_id(keyword: str, preferences: Dict) -> Optional[str]:
        return next(
            (kw_id for kw_id, kw in preferences.items() if kw == keyword), None
        )


class ItemEnterEventListener(EventListener):
    """Only when enter is pressed from an ExtensionCustomAction item"""

    def on_event(
        self, event: ItemEnterEvent, extension: FSBookmarks
    ) -> RenderResultListAction:
        option, fs_bookmark = event.get_data()
        if option == CustomActionOption.ADD_FSB:
            FSBFile().add_fs_bookmark(fs_bookmark)
        elif option == CustomActionOption.REM_FSB:
            FSBFile().remove_fs_bookmark(fs_bookmark)
        return extension.hide()
