from collections import OrderedDict
from typing import Optional

from util.functions import get_attr_str


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
            border_radius: Optional[str] = None,
            margin: Optional[str] = None,
            padding: Optional[str] = None,
            spacing: Optional[str] = None,
            text_align: Optional[str] = None,
    ):
        self.display = display  # размещение элемента: inline, block, inline-block (none, inherit, initial)
        self.overflow_x = overflow_x  # поведение при переполнении: visible, hidden, scroll, auto
        self.overflow_y = overflow_y  # поведение при переполнении: visible, hidden, scroll, auto
        self.text_overflow = text_overflow  # обрезка текста: clip, ellipsis
        self.text_align = text_align  # выравнивание текста: left, right, center, justify
        self.white_space = white_space  # перенос строки: nowrap, pre, pre-wrap, pre-line, normal
        self.scrollbar_width = scrollbar_width  # полоса прокрутки: auto, thin, none
        self.color = color  # цвет шрифта
        self.background = background  # фон: image, size, repeat, height
        # self.background_color = background_color
        self.border = border  # граница: width, color, radius
        self.border_radius = border_radius  # граница: width, color, radius
        self.margin = margin  # отступ снаружи
        self.padding = padding  # отступ внутри
        self.spacing = spacing  # отступ снаружи

    def get_html_style_str(self) -> str:
        style_dict = self._get_html_style_dict()
        style_args = [f'{k}: {v};' for k, v in style_dict.items()]
        return ' '.join(style_args)

    def _get_html_style_dict(self) -> OrderedDict:
        style = OrderedDict()
        for k, v in self._get_init_kwargs().items():
            if v is not None:
                style[k.replace('_', '-')] = v
        return style

    def _get_init_kwargs(self, skip_none: bool = True) -> dict:
        if skip_none:
            init_kwargs = dict()
            for k, v in vars(self).items():
                if v is not None:
                    init_kwargs[k] = v
            return init_kwargs
        else:
            return vars(self).copy()

    def __add__(self, other):
        props = self._get_init_kwargs()
        if other is None:
            pass
        elif isinstance(other, Style):
            props.update(other._get_init_kwargs(skip_none=True))
        else:
            raise TypeError(other)
        return Style(**props)

    def __repr__(self):
        cls = self.__class__.__name__
        attr = get_attr_str(self._get_html_style_dict())
        return f'{cls}({attr})'

    def __str__(self):
        return self.get_html_style_str()
