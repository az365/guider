from enum import Enum
from typing import Optional

from util.const import DEFAULT_FONT_SIZE, DEFAULT_FONT_PROPORTION
from util.types import Numeric


class Unit(Enum):
    Pixel = 'px'
    Char = 'ch'  # 0-symbol width
    Ephemeral = 'em'  # font size

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

    @classmethod
    def parse(cls, x: str) -> tuple:
        assert isinstance(x, str), TypeError(x)
        assert len(x) > 2, ValueError(x)
        for k, v in cls._member_map_.items():
            if x.endswith(v.value):
                unit = v
                num_str = x[:-len(v.value)]
                if '.' in num_str:
                    count = float(num_str)
                else:
                    count = int(num_str)
                return count, unit
        raise ValueError
