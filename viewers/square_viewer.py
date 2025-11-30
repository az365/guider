from typing import Tuple, Union, Iterable, Optional

from util.const import MAX_MD_ROW_LEN
from util.functions import crop, get_repr
from visual import Unit, Size1d, Size2d, Style, TagType
from views.formatted_view import FormattedView
from views.square_view import SquareView
from viewers.tree_viewer import TreeViewer

HINT_LEN = MAX_MD_ROW_LEN
MIN_SIZE_FOR_ITEMS_VIEW = Size1d('1em')
TITLE_STYLE = Style(color='white', background='grey')
ITEM_STYLE = Style(
    overflow_x='hidden', overflow_y='hidden',
    background='yellow', border='solid',
)
KEY_STYLE = Style(color='grey')


class SquareViewer(TreeViewer):
    def __init__(self, size: Union[Size2d, Tuple[float, float]], style: Optional[Style] = None, max_depth: int = 5):
        super().__init__(depth=max_depth)
        self._size = None
        self._style = None
        self.set_size(size)
        self.set_style(style)

    def get_size(self) -> Size2d:
        return self._size

    def set_size(self, size: Union[Size2d, Tuple[float, float]]):
        if isinstance(size, Size2d):
            pass
        elif isinstance(size, Iterable):
            size = Size2d(*size)
        else:
            raise TypeError(size)
        self._size = size

    size = property(get_size, set_size)

    def get_style(self) -> Style:
        return self._style

    def set_style(self, style: Union[Style, dict, str]):
        if style is None:
            style = Style()
        elif isinstance(style, Style):
            # pass
            style = Style(**style._get_init_kwargs())
        elif isinstance(style, dict):
            style = Style(**style)
        elif isinstance(style, str):
            style = Style.from_str(style)
        else:
            raise TypeError(style)
        self._style = style

    style = property(get_style, set_style)

    def get_view(
            self,
            obj,
            include_title: bool = True,
            size: Optional[Size2d] = None,
            style: Optional[Style] = None,
            depth: Optional[int] = None,
            prefix: Optional[FormattedView] = None,
            tag: Optional[TagType] = None,
            ordered: Optional[bool] = False,
    ) -> SquareView:
        if size is None:
            size = self.size
        if style is None:
            style = self.style
        elif self.style:
            style = self.style + style
        if depth is None:
            depth = self.depth
        lines_count = self.size.get_lines_count()
        line_len = self.size.get_line_len()
        if lines_count < 0.3 or line_len < 1 or depth < 0 or obj is None:  # show placeholder instead of content
            view = self._get_empty_view(obj, size=size, style=style)
        elif lines_count < 1.5:
            view = self._get_one_line_view(obj, size=size, style=style)
        elif lines_count < 4:
            view = self._get_three_lines_view(obj, size=size, style=style)
        elif size.x >= size.y:
            view = self._get_horizontal_view(obj, size=size, style=style, depth=depth, include_title=include_title)
        else:
            view = self._get_vertical_view(obj, size=size, style=style, depth=depth, include_title=include_title)
        return view

    def _get_empty_view(self, obj, size: Size2d, style: Style) -> SquareView:
        one_line = self._get_one_line(obj)
        style = style + Style(background='gray')
        return SquareView([''], tag=None, size=size, style=style, hint=one_line)

    def _get_one_line_view(self, obj, size: Size2d, style: Style) -> SquareView:
        one_line = self._get_one_line(obj)
        if size is None:
            size = self.size
        if size.get_lines_count() < 0.9:
            font_scale = size.y.get_for_units(Unit.Ephemeral)
            tag = TagType.Font.create(size=str(font_scale))
        else:
            tag = None
        return SquareView([one_line], tag=tag, size=size, style=style, hint=one_line)

    def _get_three_lines_view(self, obj, size: Size2d, style: Style) -> SquareView:
        cls_name = obj.__class__.__name__
        line1 = self._get_one_line(obj)
        line2 = self._get_one_line(obj)
        hint = self._get_one_line(obj)
        return SquareView([cls_name, line1, line2], tag=None, size=size, style=style, hint=hint)

    def _get_vertical_view(self, obj, size: Size2d, style: Style, depth: int, include_title: bool) -> SquareView:
        return self._get_directional_view(obj, size=size, style=style, vertical=True, depth=depth, include_title=include_title)

    def _get_horizontal_view(self, obj, size: Size2d, style: Style, depth: int, include_title: bool) -> SquareView:
        return self._get_directional_view(obj, size=size, style=style, vertical=False, depth=depth, include_title=include_title)

    def _get_directional_view(self, obj, size: Size2d, style: Style, vertical: bool, depth: int, include_title: bool) -> SquareView:
        one_line = self._get_one_line(obj)
        if include_title:
            title_size = Size2d(x=size.x, y='1em')
            content_size = Size2d(x=size.x, y=size.y-title_size.y)
            title_hint = f'title: {one_line}'
            title_view = SquareView([one_line], tag=TagType.Paragraph, size=title_size, style=TITLE_STYLE, hint=title_hint)
        else:
            title_size, title_view = None, None
            content_size = size
        if content_size.y_size >= MIN_SIZE_FOR_ITEMS_VIEW:
            if isinstance(obj, SquareView):
                content_view = obj
            elif isinstance(obj, FormattedView):
                content_view = SquareView(obj, tag=None, size=content_size, style=None, hint=None)
            elif isinstance(obj, str):
                content_view = SquareView(obj, tag=TagType.Paragraph, size=content_size, style=None, hint=get_repr(obj))
            else:
                content_view = self._get_items_view(obj, content_size=content_size, vertical=vertical, depth=depth)
        else:
            content_view = None
        entire_view_items = list()
        for i in (title_view, content_view):
            if i is not None:
                entire_view_items.append(i)
        hint = one_line.crop(HINT_LEN, inplace=False)
        if entire_view_items:
            entire_view = SquareView(entire_view_items, tag=TagType.Div, size=size, style=style, hint=hint)
        else:
            style_for_empty = style + Style(background='silver')
            entire_view = SquareView([], tag=TagType.Div, size=size, style=style_for_empty, hint=hint)
        return entire_view

    def _get_items_view(self, obj, content_size: Size2d, vertical: bool, depth: int):
        items = self._get_key_value_pairs_from_obj(obj)
        count = len(items)
        if count == 0:
            squared_items = list()
        elif count == 1 and isinstance(items[0], FormattedView):
            squared_items = [items[0]]
        else:
            spacing_1d = Size1d(3, unit=Unit.Pixel)
            spacing_2d = spacing_1d * spacing_1d
            display_mode = 'block' if vertical else 'inline-block'
            hor = not vertical
            i_size = content_size.divide_numeric(count, horizontal=hor, vertical=vertical, rounding=True) - spacing_2d
            i_style = ITEM_STYLE + Style(display=display_mode, spacing=str(spacing_1d))
            key_size = Size2d(x=i_size.x, y='1em')
            value_size = Size2d(x=i_size.x, y=i_size.y - key_size.y)
            value_style = Style()
            squared_items = list()
            for k, v in items:
                key_hint = f'key: {k}'
                key_view = SquareView([k], tag=None, size=key_size, style=KEY_STYLE, hint=key_hint)
                if isinstance(v, FormattedView):
                    value_view = v
                else:
                    value_view = self.get_view(v, size=value_size, style=value_style, depth=depth - 1)
                i_squared = SquareView([key_view, value_view], tag=None, size=i_size, style=i_style, hint=None)
                squared_items.append(i_squared)
        items_hint = crop(get_repr(obj), max_len=HINT_LEN)
        return SquareView(squared_items, tag=TagType.Div, size=content_size, style=None, hint=items_hint)

    def _get_key_value_pairs_from_obj(self, obj) -> list[tuple]:
        if isinstance(obj, str):
            items = [FormattedView([obj], TagType.Paragraph)]
        elif isinstance(obj, dict):
            items = list(obj.items())
        elif isinstance(obj, Iterable) and not isinstance(obj, str):
            items = list(enumerate(obj))
        else:
            items = list(self._get_wrapped_object(obj).get_props().items())
        return items
