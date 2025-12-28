from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Optional, Union, Callable

from util.const import DEFAULT_FONT_SIZE, DEFAULT_FONT_PROPORTION
from util.types import Numeric, NUMERIC
from abstract.common_abstract import CommonAbstract
from visual.unit import Unit

Native = CommonAbstract

DEFAULT_UNIT = Unit.Pixel


class AbstractSize(CommonAbstract, ABC):
    def __init__(
            self,
            unit: Unit = DEFAULT_UNIT,
            font_size: int = DEFAULT_FONT_SIZE,
            font_proportion: float = DEFAULT_FONT_PROPORTION,
    ):
        if not isinstance(unit, Unit):
            unit = Unit(unit)
        self._unit = unit

        self.font_size = font_size
        self.font_proportion = font_proportion

    def get_unit(self) -> Optional[Unit]:
        return self._unit

    def set_unit(self, unit: Unit):
        self._unit = unit

    unit = property(get_unit, set_unit)

    @abstractmethod
    def get_for_units(self, unit: Unit):
        pass

    def _get_font_kwargs(self) -> OrderedDict:
        return OrderedDict(font_size=self.font_size, font_proportion=self.font_proportion)

    def _set_font_kwargs(self, font_kwargs: dict, skip_empty: bool = True):
        if font_kwargs.get('font_size') or not skip_empty:
            self.font_size = font_kwargs['font_size']
        if font_kwargs.get('font_proportion') or not skip_empty:
            self.font_proportion = font_kwargs['font_proportion']

    @abstractmethod
    def _compare(self, other, cmp: Callable):
        pass

    def __eq__(self, other):
        return self._compare(other, cmp=lambda a, b: a == b)

    def __ne__(self, other):
        return self._compare(other, cmp=lambda a, b: a != b)

    def __lt__(self, other):
        return self._compare(other, cmp=lambda a, b: a < b)

    def __le__(self, other):
        return self._compare(other, cmp=lambda a, b: a <= b)

    def __gt__(self, other):
        return self._compare(other, cmp=lambda a, b: a > b)

    def __ge__(self, other):
        return self._compare(other, cmp=lambda a, b: a >= b)

    def __repr__(self):
        return str(self)

SizeOrNumeric = Union[AbstractSize, Numeric, str, None]


class Size1d(AbstractSize):
    def __init__(
            self,
            x: SizeOrNumeric,
            unit: Unit = DEFAULT_UNIT,
            font_size: int = DEFAULT_FONT_SIZE,
            font_proportion: float = DEFAULT_FONT_PROPORTION,
    ):
        super().__init__(unit=unit, font_size=font_size, font_proportion=font_proportion)
        self._x = None
        self.set_value(x)

    def get_numeric(self) -> Optional[Numeric]:
        return self._x

    def set_numeric(self, x: Optional[Numeric]):
        assert isinstance(x, NUMERIC) or x is None, TypeError(x)
        self._x = x

    numeric = property(get_numeric, set_numeric)

    def get_size(self) -> AbstractSize:
        return Size1d(self.numeric, unit=self.unit, **self._get_font_kwargs())

    def set_size(self, x: AbstractSize):
        assert isinstance(x, Size1d), TypeError(repr(x))
        self._unit = x.unit
        self._x = x.numeric
        self._set_font_kwargs(x._get_font_kwargs())

    size = property(get_size, set_size)

    def get_unit(self) -> Optional[Unit]:
        return self._unit

    def set_unit(self, unit: Unit):
        if self._unit is None:
            self._unit = unit
        elif self._unit == unit:
            pass
        else:
            self._x = Unit.translate(self._x, src=self._unit, dst=unit)
            self._unit = unit

    unit = property(get_unit, set_unit)

    def set_value(self, x: SizeOrNumeric):
        if isinstance(x, Size1d):
            self.set_size(x)
        elif isinstance(x, NUMERIC) or x is None:
            self.set_numeric(x)
        elif isinstance(x, str):
            self.numeric, self._unit = Unit.parse(x)
        else:
            raise TypeError(x)

    def get_for_units(self, unit: Unit) -> AbstractSize:
        translated = Unit.translate(self.numeric, src=self.unit, dst=unit, **self._get_font_kwargs())
        return Size1d(translated, unit=unit, **self._get_font_kwargs())

    def get_lines_count(self, round_factor: int = 1) -> Optional[Numeric]:
        if self.numeric is not None:
            y = self.get_for_units(Unit.Ephemeral).numeric
            return round(y, round_factor)

    def get_line_len(self, round_factor: int = 0) -> Optional[Numeric]:
        if self.numeric is not None:
            x = self.get_for_units(Unit.Char).numeric
            return round(x, round_factor)

    def _compare(self, other: AbstractSize, cmp: Callable):
        assert isinstance(other, Size1d), TypeError(other)
        if self.unit == other.unit:
            a = self.numeric
            b = other.numeric
        else:
            a = self.get_for_units(DEFAULT_UNIT)
            b = other.get_for_units(DEFAULT_UNIT)
        return cmp(a, b)

    def __add__(self, other: SizeOrNumeric):
        if isinstance(other, Size1d):
            other_unit = other.unit
            other_numeric = other.numeric
        elif isinstance(other, NUMERIC) or other is None:
            other_unit = None
            other_numeric = other
        elif isinstance(other, str):
            other_numeric, other_unit = Unit.parse(other)
        else:
            raise TypeError(other)
        if self.numeric is None or other_numeric is None:
            sum_numeric = None
        elif other_unit is None or other_unit == self.unit:
            sum_numeric = self.numeric + other_numeric
        else:
            other_numeric = Unit.translate(other_numeric, src=other_unit, dst=self.unit, **self._get_font_kwargs())
            sum_numeric = self.numeric + other_numeric
        sum_size = Size1d(sum_numeric, unit=self.unit or other_unit, **self._get_font_kwargs())
        return sum_size

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        if self.numeric is None:
            neg_numeric = None
        else:
            neg_numeric = -self.numeric
        return Size1d(neg_numeric, unit=self.unit, **self._get_font_kwargs())

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.modify(x=self.numeric*other)
        elif isinstance(other, Size1d):
            return Size2d(self.size, other.size, **self._get_font_kwargs())
        else:
            raise TypeError(repr(other))

    def __truediv__(self, other):
        assert isinstance(other, (int, float)), TypeError(repr(other))
        x = self.numeric / other
        return Size1d(x, unit=self.unit, **self._get_font_kwargs())

    def __floordiv__(self, other):
        assert isinstance(other, (int, float)), TypeError(repr(other))
        x = self.numeric // other
        return Size1d(x, unit=self.unit, **self._get_font_kwargs())

    def __round__(self, n=None):
        if n is None:
            x = int(self._x)
        else:
            x = round(self._x, n)
        return Size1d(x, unit=self.unit, **self._get_font_kwargs())

    def __str__(self):
        if self.numeric is None:
            return ''
        else:
            unit = '' if self.unit is None else self.unit.value
            return f'{self.numeric}{unit}'


SizeOrNumeric = Union[Size1d, Numeric, str, None]


class Size2d(AbstractSize):
    def __init__(
            self,
            x: SizeOrNumeric,
            y: SizeOrNumeric,
            unit: Unit = DEFAULT_UNIT,
            font_size: int = DEFAULT_FONT_SIZE,
            font_proportion: float = DEFAULT_FONT_PROPORTION,
    ):
        super().__init__(unit=unit, font_size=font_size, font_proportion=font_proportion)
        self._x = None
        self._y = None
        self.set_x(x)
        self.set_y(y)

    def get_x_numeric(self) -> Numeric:
        return self._x

    def set_x_numeric(self, x: Numeric):
        assert isinstance(x, NUMERIC) or x is None, TypeError(x)
        self._x = x

    x_numeric = property(get_x_numeric, set_x_numeric)

    def get_y_numeric(self) -> Optional[Numeric]:
        return self._y

    def set_y_numeric(self, y: Optional[Numeric]):
        assert isinstance(y, NUMERIC) or y is None, TypeError(y)
        self._y = y

    y_numeric = property(get_y_numeric, set_y_numeric)

    def get_x_size(self) -> Size1d:
        return Size1d(self.x_numeric, unit=self.unit, **self._get_font_kwargs())

    def set_x_size(self, x: Size1d):
        assert isinstance(x, Size1d), TypeError(x)
        self.unit = x.unit  # scaling y-size for new unit-scale
        self.x_numeric = x.numeric

    x_size = property(get_x_size, set_x_size)

    def get_y_size(self) -> Size1d:
        return Size1d(self.y_numeric, unit=self.unit, **self._get_font_kwargs())

    def set_y_size(self, y: Size1d):
        assert isinstance(y, Size1d), TypeError(y)
        self.unit = y.unit  # scaling x-size for new unit-scale
        self.y_numeric = y.numeric

    y_size = property(get_y_size, set_y_size)

    def get_x(self) -> Size1d:
        return self.get_x_size()

    def set_x(self, x: SizeOrNumeric):
        if isinstance(x, Size1d):
            self.set_x_size(x)
        elif isinstance(x, NUMERIC) or x is None:
            self.set_x_numeric(x)
        elif isinstance(x, str):
            x_size = self.get_x_size()
            x_size.set_value(x)
            self.set_x_size(x_size)
        else:
            raise TypeError(x)

    x = property(get_x, set_x)

    def get_y(self) -> Size1d:
        return self.get_y_size()

    def set_y(self, y: SizeOrNumeric):
        if isinstance(y, Size1d):
            self.set_y_size(y)
        elif isinstance(y, NUMERIC) or y is None:
            self.set_y_numeric(y)
        elif isinstance(y, str):
            y_size = self.get_y_size()
            y_size.set_value(y)
            self.set_y_size(y_size)
        else:
            raise TypeError(y)

    y = property(get_y, set_y)

    def get_unit(self) -> Optional[Unit]:
        return self._unit

    def set_unit(self, unit: Unit):
        self.x_numeric = Unit.translate(self.x_numeric, src=self._unit, dst=unit)
        self.y_numeric = Unit.translate(self.y_numeric, src=self._unit, dst=unit)
        self._unit = unit

    unit = property(get_unit, set_unit)

    def get_html_width(self) -> str:
        if self.x_numeric is None:
            return 'auto'
        else:
            unit = self.unit.value if self.unit else ''
            return f'{self.x_numeric}{unit}'

    def get_html_height(self) -> str:
        if self.y_numeric is None:
            return 'auto'
        else:
            unit = self.unit.value if self.unit else ''
            return f'{self.y_numeric}{unit}'

    def get_for_units(self, unit: Unit) -> AbstractSize:
        x = self.x_size.get_for_units(unit)
        y = self.y_size.get_for_units(unit)
        return Size2d(x, y, unit=unit, **self._get_font_kwargs())

    def get_lines_count(self, round_factor: int = 1) -> Optional[Numeric]:
        return self.y_size.get_lines_count(round_factor)

    def get_line_len(self, round_factor: int = 0) -> Optional[Numeric]:
        return self.x_size.get_line_len(round_factor)

    def divide_numeric(self, other: Numeric, horizontal: bool = True, vertical: bool = True, rounding: bool = False):
        x = self.x / other if horizontal else self.x
        y = self.y / other if vertical else self.y
        if rounding:
            x = int(x.numeric)
            y = int(y.numeric)
        return Size2d(x, y, unit=self.unit, **self._get_font_kwargs())

    def divide_2d(self, other: AbstractSize, rounding: bool = False):
        assert isinstance(other, Size2d), TypeError(repr(other))
        assert other.unit is None, ValueError(f'unit must not be set, got {repr(other.unit)}')
        x = self.x / other.x_numeric
        y = self.y / other.y_numeric
        if rounding:
            x = int(x.numeric)
            y = int(y.numeric)
        return Size2d(x, y, unit=self.unit, **self._get_font_kwargs())

    def get_area_numeric(self) -> float:
        return self.x_numeric * self.y_numeric

    def _compare(self, other: AbstractSize, cmp: Callable):
        assert isinstance(other, Size2d), TypeError(other)
        a = self.get_area_numeric()
        b = other.get_for_units(self.unit).get_area_numeric()
        return cmp(a, b)

    def __add__(self, other: AbstractSize):
        assert isinstance(other, Size2d)
        x_sum = self.x_size + other.x_size
        y_sum = self.y_size + other.y_size
        return self.__class__(x_sum, y_sum)

    def __neg__(self):
        x_neg = -self.x_size
        y_neg = -self.y_size
        return self.__class__(x_neg, y_neg)

    def __sub__(self, other: AbstractSize):
        assert isinstance(other, Size2d)
        return self.__add__(-other)

    def __truediv__(self, other):
        if isinstance(other, NUMERIC):
            is_horizontal = self.x > self.y
            return self.divide_numeric(other, horizontal=is_horizontal, vertical=not is_horizontal, rounding=False)
        elif isinstance(other, Size2d):
            return self.divide_2d(other, rounding=False)
        else:
            raise TypeError(repr(other))

    def __floordiv__(self, other):
        if isinstance(other, NUMERIC):
            is_horizontal = self.x > self.y
            return self.divide_numeric(other, horizontal=is_horizontal, vertical=not is_horizontal, rounding=True)
        elif isinstance(other, Size2d):
            return self.divide_2d(other, rounding=True)
        else:
            raise TypeError(repr(other))

    def __round__(self, n=None):
        if n is None:
            x = int(self._x)
            y = int(self._y)
        else:
            x = round(self._x, n)
            y = round(self._y, n)
        return Size2d(x, y, unit=self.unit, **self._get_font_kwargs())

    def __str__(self):
        x = '-' if self.x_numeric is None else self.x_numeric
        y = '-' if self.y_numeric is None else self.y_numeric
        unit = '' if self.unit is None else self.unit.value
        return f'{x}x{y}{unit}'
