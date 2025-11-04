from enum import Enum
from collections import OrderedDict
from typing import Optional, Iterable, Union

from views.formatted_view import FormattedView
from wrappers.functions import get_attr_str


class Unit(Enum):
    Pixel = 'px'
    Char = 'ch'  # ширина символа O
    Ephemeral = 'em'  # размер шрифта


class Size:
    def __init__(self, x, y, unit: Unit = Unit.Pixel, font_size: int = 16):
        self._x = x
        self._y = y
        if not isinstance(unit, Unit):
            unit = Unit(unit)
        self.unit = unit

        self.font_size = font_size

    def get_html_width(self) -> str:
        return f'{self._x}{self.unit.value or ""}'

    def get_html_height(self) -> str:
        return f'{self._y}{self.unit.value or ""}'

    def get_for_units(self, unit: Unit):
        if unit == self.unit:
            return self
        else:
            x, y = None, None
        if unit == Unit.Pixel:
            if self.unit == Unit.Ephemeral:
                x = self._x * self.font_size
                y = self._y * self.font_size
        if unit == Unit.Ephemeral:
            if self.unit == Unit.Pixel:
                x = self._x / self.font_size
                y = self._y / self.font_size
        if x is not None and y is not None:
            return Size(x, y, unit)
        else:
            raise NotImplementedError

    def __repr__(self):
        cls = self.__class__.__name__
        attr = get_attr_str(vars(self))
        return f'{cls}({attr})'

    def __str__(self):
        return repr(self)


class Style:
    def __init__(
            self,
            display: Optional[str] = None,
            overflow_x: Optional[str] = None,
            overflow_y: Optional[str] = None,
            text_overflow: Optional[str] = None,
            white_space: Optional[str] = None,
            scrollbar_width: Optional[str] = None,
            color: Optional[str] = None,
            background: Optional[str] = None,
            # background_color: Optional[str] = None,
            border: Optional[str] = None,
            margin: Optional[str] = None,
            padding: Optional[str] = None,

    ):
        self.display = display  # размещение элемента: inline, block, inline-block (none, inherit, initial)
        self.overflow_x = overflow_x  # поведение при переполнении: visible, hidden, scroll, auto
        self.overflow_y = overflow_y  # поведение при переполнении: visible, hidden, scroll, auto
        self.text_overflow = text_overflow  # обрезка текста: clip, ellipsis
        self.white_space = white_space  # перенос строки: nowrap, pre, pre-wrap, pre-line, normal
        self.scrollbar_width = scrollbar_width  # полоса прокрутки: auto, thin, none
        self.color = color  # цвет шрифта
        self.background = background  # фон: image, size, repeat, height
        # self.background_color = background_color
        self.border = border  # граница: width, color, radius
        self.margin = margin  # отступ снаружи
        self.padding = padding  # отступ внутри

    def get_html_style_str(self) -> str:
        style_dict = self._get_html_style_dict()
        style_args = [f'{k}: {v};' for k, v in style_dict.items()]
        return ' '.join(style_args)

    def _get_html_style_dict(self) -> OrderedDict:
        style = OrderedDict()
        # style['color'] = self.color
        # style['background_color'] = self.background_color
        # style['border'] = self.border
        # style['margin'] = self.border
        # style['padding'] = self.border
        for k, v in vars(self).items():
            if v is not None:
                style[k.replace('_', '-')] = v
        return style

    def __repr__(self):
        cls = self.__class__.__name__
        attr = get_attr_str(self._get_html_style_dict())
        return f'{cls}({attr})'

    def __str__(self):
        return self.get_html_style_str()


class SquareView(FormattedView):
    def __init__(self, data: Iterable, tag, size: Size, style: Style, hint: str):
        super().__init__(data, tag)
        self.size = size
        self.style = style or Style()
        self.hint = hint  # ToDo: or move to FormattingTag ?

    def get_html_lines(self) -> Iterable[str]:
        yield self.get_html_open_tag()
        yield from super().get_html_lines()
        yield self.get_html_close_tag()

    def get_html_open_tag(self) -> str:
        style = self.get_html_style_str()
        return f'<div style="{style}">'

    def get_html_close_tag(self) -> str:
        return '</div>'

    def get_html_width(self) -> Optional[str]:
        return self.size.get_html_width()

    def get_html_height(self) -> Optional[str]:
        return self.size.get_html_height()

    def get_html_title(self) -> Optional[str]:
        if self.hint:
            return self.hint.replace('"', '``')

    def get_html_style_str(self) -> str:
        style_dict = self._get_html_style_dict()
        style_args = [f'{k}: {v};' for k, v in style_dict.items()]
        return ' '.join(style_args)

    def _get_html_style_dict(self) -> Union[OrderedDict, dict]:
        style = self.style._get_html_style_dict()
        if self.get_html_width():
            style['width'] = self.get_html_width()
        if self.get_html_height():
            style['height'] = self.get_html_height()
        if self.get_html_title():
            style['title'] = self.get_html_title()
        return style
