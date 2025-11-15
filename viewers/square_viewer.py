from typing import Tuple, Union, Iterable, Optional

from visual.unit import Unit
from visual.size import Size1d, Size2d
from visual.style import Style
from visual.formatting_tag import TagType
from views.formatted_view import FormattedView
from views.square_view import SquareView
from viewers.tree_viewer import TreeViewer


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
        if lines_count < 0.3 or line_len < 1 or depth < 0 or obj is None:
            view = self._get_empty_view(obj, size=size, style=style)
        elif lines_count < 1.5:
            view = self._get_one_line_view(obj, size=size, style=style)
        elif lines_count < 4:
            view = self._get_three_lines_view(obj, size=size, style=style)
        elif size.x >= size.y:
            view = self._get_horizontal_view(obj, size=size, style=style, depth=depth)
        else:
            view = self._get_vertical_view(obj, size=size, style=style, depth=depth)
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

    def _get_vertical_view(self, obj, size: Size2d, style: Style, depth: int) -> SquareView:
        return self._get_items_view(obj, size=size, style=style, vertical=True, depth=depth)

    def _get_horizontal_view(self, obj, size: Size2d, style: Style, depth: int) -> SquareView:
        return self._get_items_view(obj, size=size, style=style, vertical=False, depth=depth)

    def _get_items_view(self, obj, size: Size2d, style: Style, vertical: bool, depth: int):
        one_line = self._get_one_line(obj)
        spacing = Size1d(3, unit=Unit.Pixel)
        items = self._get_items_from_obj(obj)
        if len(items) == 0:
            squared_items = list()
        elif len(items) == 1 and isinstance(items[0], FormattedView):
            squared_items = items[0]
        else:
            if vertical:
                y_i = int(size.get_for_units(Unit.Pixel)._y / len(items)) - spacing
                x_i = size.get_for_units(Unit.Pixel)._x - spacing
                display_mode = 'block'
            else:
                x_i = int(size.get_for_units(Unit.Pixel)._x / len(items)) - spacing
                y_i = size.get_for_units(Unit.Pixel)._y - spacing
                display_mode = 'inline-block'
            i_size = Size2d(x_i, y_i)
            i_style = style + Style(
                display=display_mode,
                overflow_x='hidden', overflow_y='hidden',
                spacing=spacing,
                background='yellow', border='solid',
            )
            squared_items = list()
            for i in items:
                i_squared = self.get_view(i, size=i_size, style=i_style, depth=depth - 1)
                squared_items.append(i_squared)
        return SquareView(squared_items, tag=None, size=size, style=style, hint=one_line)

    def _get_items_from_obj(self, obj) -> list[tuple]:
        if isinstance(obj, str):
            items = [FormattedView([obj], TagType.Paragraph)]
        elif isinstance(obj, dict):
            items = list(obj.items())
        elif isinstance(obj, Iterable) and not isinstance(obj, str):
            items = list(obj)
        else:
            items = list(self.get_wrapped_object(obj).get_props().items())
        return items
