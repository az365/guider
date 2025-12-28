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
DETAILED_CAPTION_STYLE = Style(
    text_overflow='ellipsis',
)
DEFAULT_AXIS_WIDTH = Size1d(75, Unit.Pixel)
DEFAULT_PADDING = Size2d(10, 10, Unit.Pixel)


class BarChartViewer(SquareViewer):
    def __init__(
            self,
            size: Union[Size2d, Tuple[float, float]] = DEFAULT_CHART_SIZE,
            style: Optional[Style] = DEFAULT_CHART_STYLE,
            bar_style: str = DEFAULT_BAR_STYLE,
            scale_x: Optional[float] = None,
            axis_width: Size1d = DEFAULT_AXIS_WIDTH,
            max_depth: Optional[int] = None,
            padding: Optional[Size2d] = DEFAULT_PADDING,
    ):
        super().__init__(size=size, style=style, max_depth=max_depth)
        self.axis_width = axis_width
        self.bar_style = bar_style
        self.scale_x = scale_x
        self.padding = padding or Size2d(0, 0)

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
            bar_style: Style = DEFAULT_BAR_STYLE,
            padding: Optional[Size2d] = None,
            captions_for_axis: Optional[dict] = None,
            captions_for_values: Optional[dict] = None,
    ) -> SquareView:
        assert isinstance(obj, dict), TypeError(obj)
        if size is None:
            size = self.size
        if style is None:
            style = self.style
        if scale_x is None:
            scale_x = self.scale_x
        if padding is None:
            padding = self.padding
        chart_size = size - padding * 2
        bar_chart_view = SquareView.vertical([], size=chart_size, style=style)
        bars_count = len(obj)
        row_height = size.y / bars_count
        row_frame_size = Size2d(chart_size.x, row_height)
        bar_frame_size = Size2d(row_frame_size.x - self.axis_width, row_height)
        mark_size = Size2d(self.axis_width, row_height)
        if scale_x is None:
            max_value = get_max_value(obj, sum_secondary=True)
            max_value_rounded = smart_round(max_value, upper=True)
            scale_x = bar_frame_size.x / max_value_rounded
            scale_x = int(scale_x.numeric)
        for k, v in obj.items():
            row = self._get_bar_row(
                row_name=k,
                value=v,
                scale_x=scale_x,
                row_frame_size=row_frame_size,
                mark_size=mark_size,
                bar_style=bar_style,
                captions_for_axis=captions_for_axis,
                captions_for_values=captions_for_values,
            )
            bar_chart_view.data.append(row)
        if padding.x or padding.y:
            padding_y = SquareView([], TagType.Div, size=Size2d(size.x, padding.y))
            padding_x = SquareView([], TagType.Div, size=Size2d(padding.x, chart_size.y))
            chart_row_view = SquareView.horizontal(
                data=[padding_x, bar_chart_view, padding_x],
                size=Size2d(size.x, chart_size.y),
            )
            bar_chart_view = SquareView.vertical(
                data=[padding_y, chart_row_view, padding_y],
                size=size,
                style=style,
            )
        assert isinstance(bar_chart_view, SquareView)
        return bar_chart_view

    def _get_bar_row(
            self,
            row_name: str,
            value: Union[float, dict],
            scale_x: float,
            row_frame_size: Size2d,
            mark_size: Size2d,
            bar_style: Style,
            captions_for_axis: Optional[dict] = None,
            captions_for_values: Optional[dict] = None,
    ) -> SquareView:
        bar_frame_size = Size2d(row_frame_size.x - self.axis_width, row_frame_size.y)
        if isinstance(value, (int, float)):
            sum_value = value
        elif isinstance(value, dict):
            sum_value = sum(value.values())
        else:
            raise TypeError(value)
        if self.axis_width:
            caption_text = str(sum_value)
            if captions_for_axis:
                detailed_caption_text = captions_for_axis.get(row_name)
                row_hint = f'{row_name}: {detailed_caption_text}'
                detailed_caption = SquareView(
                    detailed_caption_text,
                    tag=TagType.Paragraph.create(style='font-size=-2;'),
                    style=DETAILED_CAPTION_STYLE,
                    hint=detailed_caption_text,
                )
            else:
                row_hint = row_name
                detailed_caption = None
            axis_label = SquareView.vertical(
                data=[row_name, detailed_caption],
                size=mark_size,
                style=MARK_STYLE,
                hint=row_hint,
            )
            bar_style.display = 'inline-block'
            axis_label.style.display = 'inline-block'
        else:
            caption_text = f'{row_name}: {sum_value}'
            detailed_caption = None
            axis_label = None
        if captions_for_values:
            hint = f'{row_name}: {sum_value} {captions_for_values.get(row_name)}'
        else:
            hint = f'{row_name}: {sum_value}'
        bar_width = sum_value * scale_x
        bar_size = Size2d(bar_width, bar_frame_size.y)
        caption_size = Size2d(row_frame_size.x - self.axis_width - bar_size.x, bar_frame_size.y)
        bar = SquareView(
            data=[],
            tag=TagType.Span,
            size=bar_size,
            style=bar_style,
            hint=hint,
        )
        caption = SquareView.horizontal(
            [caption_text, detailed_caption],
            size=caption_size,
        )
        row = SquareView.horizontal([axis_label, bar, caption], size=row_frame_size, style=ROW_STYLE, hint=hint)
        assert isinstance(row, SquareView)
        return row
