from typing import Optional, Tuple, Union

from util.functions import get_max_value, smart_round
from views.formatted_view import FormattedView
from visual import Style, Unit, Size1d, Size2d, TagType
from views.square_view import SquareView
from viewers.square_viewer import SquareViewer


DEFAULT_CHART_COLOR = 'grey'
DEFAULT_BAR_COLOR = 'silver'
DEFAULT_CHART_SIZE = Size2d(480, 270, Unit.Pixel)
DEFAULT_CHART_STYLE = Style(background=DEFAULT_CHART_COLOR)
DEFAULT_BAR_STYLE = Style(
    background=DEFAULT_BAR_COLOR,
    overflow_x='hidden', overflow_y='hidden',
    text_overflow='ellipsis', text_align='right', white_space='nowrap',
)
MARK_STYLE = Style(
    overflow_x='hidden', overflow_y='hidden',
    text_overflow='ellipsis', text_align='right', white_space='nowrap',
)
ROW_STYLE = Style(
    display='inline-block',
    overflow_x='hidden', overflow_y='hidden', white_space='nowrap',
)
DEFAULT_AXIS_WIDTH = Size1d(75, Unit.Pixel)


class BarChartViewer(SquareViewer):
    def __init__(
            self,
            size: Union[Size2d, Tuple[float, float]] = DEFAULT_CHART_SIZE,
            style: Optional[Style] = DEFAULT_CHART_STYLE,
            bar_style: str = DEFAULT_BAR_STYLE,
            scale_x: Optional[float] = None,
            axis_width: Size1d = DEFAULT_AXIS_WIDTH,
            max_depth: Optional[int] = None,
    ):
        super().__init__(size=size, style=style, max_depth=max_depth)
        self.axis_width = axis_width
        self.bar_style = bar_style
        self.scale_x = scale_x

    def get_view(
            self,
            obj: dict,
            include_title: bool = True,
            size: Optional[Size2d] = None,
            style: Optional[Style] = None,
            depth: Optional[int] = None,
            prefix: Optional[FormattedView] = None,
            tag: Optional[TagType] = None,
            ordered: Optional[bool] = False,
            scale_x: Optional[float] = None,
            bar_style: Style = DEFAULT_BAR_STYLE
    ) -> SquareView:
        assert isinstance(obj, dict)
        if size is None:
            size = self.size
        if style is None:
            style = self.style
        if scale_x is None:
            scale_x = self.scale_x
        bar_chart_view = SquareView(
            data=[],
            tag=TagType.Div,
            size=size,
            style=style,
            hint=None,
        )
        bars_count = len(obj)
        row_height = size.y / bars_count
        row_frame_size = Size2d(size.x, row_height)
        bar_frame_size = Size2d(row_frame_size.x - self.axis_width, row_height)
        mark_size = Size2d(self.axis_width, row_height)
        if scale_x is None:
            max_value = get_max_value(obj)
            max_value_rounded = smart_round(max_value, upper=True)
            scale_x = bar_frame_size.x / max_value_rounded
            scale_x = int(scale_x.numeric)
        for k, v in obj.items():
            hint = f'{k}: {v}'
            if self.axis_width:
                caption = str(v)
                axis_mark = SquareView(
                    data=k,
                    tag=TagType.Div,
                    size=mark_size,
                    style=MARK_STYLE,
                    hint=k,
                )
                bar_style.display = 'inline-block'
                axis_mark.style.display = 'inline-block'
            else:
                caption = f'{k}: {v}'
                axis_mark = None
            bar_width = v * scale_x
            bar_size = Size2d(bar_width, bar_frame_size.y)
            bar = SquareView(
                data=caption,
                tag=TagType.Span,
                size=bar_size,
                style=bar_style,
                hint=hint,
            )
            if axis_mark:
                row = SquareView(
                    [axis_mark, bar],
                    tag=None,
                    size=row_frame_size,
                    style=ROW_STYLE,
                    hint=hint,
                )
            else:
                row = bar
            bar_chart_view.data.append(row)
        return bar_chart_view
