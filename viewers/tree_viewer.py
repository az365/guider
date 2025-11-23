from typing import Optional, Iterable

from util.types import COLLECTION_TYPES
from wrappers.wrapper_interface import WrapperInterface
from visual.formatting_tag import TagType
from views.formatted_view import FormattedView
from viewers.text_viewer import TextViewer
from viewers.one_line_text_viewer import OneLineTextViewer


class TreeViewer(TextViewer):
    _get_one_line = OneLineTextViewer().get_view

    def __init__(self, depth: Optional[int] = 5):
        super().__init__()
        self.depth = depth

    def get_view(
            self,
            obj,
            depth: Optional[int] = None,
            prefix: Optional[FormattedView] = None,
            tag: Optional[TagType] = None,
            ordered: Optional[bool] = False,
    ) -> FormattedView:
        wrapped_obj = self.get_wrapped_object(obj)
        one_line = self._get_one_line(wrapped_obj)
        if prefix:
            one_line = FormattedView([prefix, one_line])
        if depth is None:
            depth = self.depth
        if depth > 0:
            if isinstance(obj, dict):
                items = self._get_view_items_for_dict(obj, depth=depth-1)
            elif isinstance(obj, COLLECTION_TYPES) and not isinstance(obj, str):
                items = self._get_view_items_for_iter(obj, depth=depth-1, ordered=ordered)
            else:
                items = self._get_view_items_for_dict(wrapped_obj.get_props(), depth=depth-1)
            if ordered is None:
                ordered = not isinstance(obj, (set, dict, WrapperInterface))
            formatted_list = FormattedView(items, TagType.List.create(ordered=ordered))
            if formatted_list:
                return FormattedView([one_line, formatted_list], tag=tag)
        return FormattedView([one_line], tag=tag)

    def _get_view_items_for_dict(self, obj: dict, depth: int) -> Iterable[FormattedView]:
        font_tag_builder = TagType.Font.get_builder()
        key_font = font_tag_builder(color="gray")
        delimiter_font = font_tag_builder(color="silver")
        for k, v in obj.items():
            formatted_key = FormattedView(k, tag=key_font)
            formatted_delimiter = FormattedView(': ', tag=delimiter_font)
            formatted_view = self.get_view(
                v,
                depth=depth-1,
                prefix=formatted_key + formatted_delimiter,
                tag=TagType.ListItem.create(ordered=False),
            )
            yield formatted_view

    def _get_view_items_for_iter(self, obj: Iterable, depth: int, ordered: Optional[bool]) -> Iterable[FormattedView]:
        if ordered is None:
            ordered = not isinstance(obj, set)
        item_tag = TagType.ListItem.create(ordered=ordered)
        for i in obj:
            yield self.get_view(i, depth=depth, ordered=ordered, tag=item_tag)
