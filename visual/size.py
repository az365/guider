from enum import Enum

from wrappers.functions import get_attr_str


class Unit(Enum):
    Pixel = 'px'
    Char = 'ch'  # ширина символа 0
    Ephemeral = 'em'  # размер шрифта


class Size:
    def __init__(self, x, y, unit: Unit = Unit.Pixel, font_size: int = 16, font_proportion: float = 0.6):
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
        if unit == self.unit:
            return self
        else:
            x, y = None, None
        if unit == Unit.Pixel:
            if self.unit == Unit.Ephemeral:
                x = self._x * self.font_size
                y = self._y * self.font_size
            if self.unit == Unit.Char:
                x = self._x * self.font_size * self.font_proportion
                y = self._y * self.font_size * self.font_proportion
        if unit == Unit.Ephemeral:
            if self.unit == Unit.Pixel:
                x = self._x / self.font_size
                y = self._y / self.font_size
            if self.unit == Unit.Char:
                x = self._x / self.font_proportion
                y = self._y / self.font_proportion
        if unit == Unit.Char:
            if self.unit == Unit.Pixel:
                x = self._x / self.font_size / self.font_proportion
                y = self._y / self.font_size / self.font_proportion
            if self.unit == Unit.Ephemeral:
                x = self._x / self.font_proportion
                y = self._y / self.font_proportion
        if x is not None and y is not None:
            return Size(x, y, unit)
        else:
            raise NotImplementedError

    def get_lines_count(self, round_factor: int = 1) -> float:
        y = self.get_for_units(Unit.Ephemeral)._y
        return round(y, round_factor)

    def get_line_len(self, round_factor: int = 0) -> float:
        x = self.get_for_units(Unit.Char)._x
        return round(x, round_factor)

    def __repr__(self):
        cls = self.__class__.__name__
        attr = get_attr_str(vars(self))
        return f'{cls}({attr})'

    def __str__(self):
        return repr(self)
