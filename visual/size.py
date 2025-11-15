from enum import Enum
from typing import Optional
from collections import OrderedDict

from util.const import DEFAULT_FONT_SIZE, DEFAULT_FONT_PROPORTION
from util.types import Numeric
from util.functions import get_attr_str


class Unit(Enum):
    Pixel = 'px'
    Char = 'ch'  # ширина символа 0
    Ephemeral = 'em'  # размер шрифта

    @staticmethod
    def translate(
            x: Optional[Numeric],
            src,  # from: Unit
            dst,  # to: Unit
            font_size: int = DEFAULT_FONT_SIZE,
            font_proportion: float = DEFAULT_FONT_PROPORTION,
    ) -> Optional[Numeric]:
        if x is None:
            return None
        if src == dst:
            return x
        if not isinstance(src, Unit):
            src = Unit(src)
        if not isinstance(dst, Unit):
            dst = Unit(dst)
        x_dst = None
        if dst == Unit.Pixel:
            if src == Unit.Ephemeral:
                x_dst = x * font_size
            if src == Unit.Char:
                x_dst = x * font_size * font_proportion
        if dst == Unit.Ephemeral:
            if src == Unit.Pixel:
                x_dst = x / font_size
            if src == Unit.Char:
                x_dst = x / font_proportion
        if dst == Unit.Char:
            if src == Unit.Pixel:
                x_dst = x / font_size / font_proportion
            if src == Unit.Ephemeral:
                x_dst = x / font_proportion
        if x_dst is not None:
            return x_dst
        else:
            raise NotImplementedError([src, dst])

DEFAULT_UNIT = Unit.Pixel

class Size:
    def __init__(
            self,
            x,
            y,
            unit: Unit = DEFAULT_UNIT,
            font_size: int = DEFAULT_FONT_SIZE,
            font_proportion: float = DEFAULT_FONT_PROPORTION,
    ):
        self._x = x
        self._y = y
        if not isinstance(unit, Unit):
            unit = Unit(unit)
        self.unit = unit

        self.font_size = font_size
        self.font_proportion = font_proportion

    def get_html_width(self) -> str:
        return f'{self._x}{self.unit.value or ""}'

    def get_html_height(self) -> str:
        return f'{self._y}{self.unit.value or ""}'

    def get_for_units(self, unit: Unit):
        x = self.x_size.get_for_units(unit)
        y = self.y_size.get_for_units(unit)
        return Size(x, y, unit=unit, **self._get_font_kwargs())

    def get_lines_count(self, round_factor: int = 1) -> float:
        y = self.get_for_units(Unit.Ephemeral)._y
        return round(y, round_factor)

    def get_line_len(self, round_factor: int = 0) -> float:
        x = self.get_for_units(Unit.Char)._x
        return round(x, round_factor)

    def _get_font_kwargs(self) -> OrderedDict:
        return OrderedDict(font_size=self.font_size, font_proportion=self.font_proportion)

    def _set_font_kwargs(self, font_kwargs: dict, skip_empty: bool = True):
        if font_kwargs.get('font_size') or not skip_empty:
            self.font_size = font_kwargs['font_size']
        if font_kwargs.get('font_proportion') or not skip_empty:
            self.font_proportion = font_kwargs['font_proportion']

    def __repr__(self):
        cls = self.__class__.__name__
        attr = get_attr_str(vars(self))
        return f'{cls}({attr})'

    def __str__(self):
        return repr(self)
