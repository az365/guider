from typing import Optional, Tuple, Union
from collections import OrderedDict
from binascii import crc32

from util.const import HTML_NB_SPACE, HTML_NEW_LINE
from util.types import Numeric, NUMERIC
from util.functions import get_max_value, smart_round
from views.formatted_view import FormattedView
from visual import Style, Unit, Size1d, Size2d, TagType
from views.square_view import SquareView
from viewers.square_viewer import SquareViewer


DEFAULT_CHART_COLOR = 'grey'
DEFAULT_BAR_COLOR = 'silver'
DETAILED_CAPTION_COLOR = '#46484F'
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
    color=DETAILED_CAPTION_COLOR,
    overflow_x='hidden', overflow_y='hidden',
    text_overflow='ellipsis', white_space='normal',
    line_height=0.8, font_size='0.8em',
    padding='0.2em',
)
DEFAULT_AXIS_WIDTH = Size1d(75, Unit.Pixel)
DEFAULT_REL_BAR_WIDTH = Size1d(150, Unit.Pixel)
DEFAULT_PADDING = Size2d(10, 10, Unit.Pixel)


class BarChartViewer(SquareViewer):
    def __init__(
            self,
            size: Union[Size2d, Tuple[float, float]] = DEFAULT_CHART_SIZE,
            style: Optional[Style] = DEFAULT_CHART_STYLE,
            bar_style: str = DEFAULT_BAR_STYLE,
            scale_x: Optional[Size1d] = None,
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
            colors: Optional[dict] = None,
            depth: Optional[int] = None,
            prefix: Optional[FormattedView] = None,
            tag: Optional[TagType] = None,
            ordered: Optional[bool] = False,
            scale_x: Optional[Size1d] = None,
            bar_style: Style = DEFAULT_BAR_STYLE,
            padding: Optional[Size2d] = None,
            captions_for_axis: Optional[dict] = None,
            captions_for_values: Optional[dict] = None,
            axis_width: Optional[Size1d] = None,
    ) -> SquareView:
        assert isinstance(obj, dict), TypeError(obj)
        if size is None:
            size = self.size
        if axis_width is None:
            axis_width = self.axis_width
        if style is None:
            style = self.style
        if scale_x is None:
            scale_x = self.scale_x
        if padding is None:
            padding = self.padding
        bar_chart_view = self._get_chart_without_padding(
            obj, scale_x=scale_x,
            chart_size=size - padding * 2, axis_width=axis_width,
            style=style, bar_style=bar_style, colors=colors,
            captions_for_axis=captions_for_axis, captions_for_values=captions_for_values,
        )
        if padding.x or padding.y:
            bar_chart_view = self._get_chart_with_padding(bar_chart_view, padding)
        assert isinstance(bar_chart_view, SquareView)
        return bar_chart_view

    @staticmethod
    def _get_chart_with_padding(
            chart_view: SquareView,
            padding: Size2d,
    ) -> SquareView:
        style = chart_view.style
        chart_size = chart_view.size
        size = chart_size + padding * 2
        padding_y = SquareView([], TagType.Div, size=Size2d(size.x, padding.y))
        padding_x = SquareView([], TagType.Div, size=Size2d(padding.x, chart_size.y))
        chart_row_view = SquareView.horizontal(
            data=[padding_x, chart_view, padding_x],
            size=Size2d(size.x, chart_size.y),
        )
        view = SquareView.vertical(
            data=[padding_y, chart_row_view, padding_y],
            size=size,
            style=style,
        )
        assert isinstance(view, SquareView)
        return view

    def _get_chart_without_padding(
            self,
            obj: dict,
            chart_size: Optional[Size2d] = None,
            axis_width: Optional[Size1d] = None,
            style: Optional[Style] = None,
            scale_x: Optional[Size1d] = None,
            bar_style: Style = DEFAULT_BAR_STYLE,
            mark_style: Style = MARK_STYLE,
            captions_for_axis: Optional[dict] = None,
            captions_for_values: Optional[dict] = None,
            colors: Optional[dict] = None,
    ) -> SquareView:
        bar_chart_view = SquareView.vertical([], size=chart_size, style=style)
        if axis_width is None:
            axis_width = Size1d(0)
        bars_count = len(obj)
        row_height = chart_size.y / bars_count
        row_frame_size = Size2d(chart_size.x, row_height)
        bar_frame_size = Size2d(row_frame_size.x - axis_width, row_height)
        mark_size = Size2d(axis_width, row_height)
        if scale_x is None:
            max_value = get_max_value(obj, sum_secondary=True)
            max_value_rounded = smart_round(max_value, upper=True)
            scale_x = bar_frame_size.x / max_value_rounded
            scale_x.numeric = int(scale_x.numeric)
        for k, v in obj.items():
            row = self._get_bar_row(
                row_name=k, value=v, bar_style=bar_style, mark_style=mark_style, colors=colors,
                scale_x=scale_x, axis_width=axis_width, row_frame_size=row_frame_size, mark_size=mark_size,
                captions_for_axis=captions_for_axis, captions_for_values=captions_for_values,
            )
            bar_chart_view.data.append(row)
        return bar_chart_view

    def _get_bar_row(
            self,
            row_name: str,
            value: Union[Numeric, dict],
            scale_x: Size1d,
            axis_width: Size1d,
            row_frame_size: Size2d,
            mark_size: Size2d,
            mark_style: Style,
            bar_style: Style,
            colors: Optional[dict] = None,
            captions_for_axis: Optional[dict] = None,
            captions_for_values: Optional[dict] = None,
    ) -> SquareView:
        bar_frame_size = Size2d(row_frame_size.x - axis_width, row_frame_size.y)
        if isinstance(value, NUMERIC):
            sum_value = value
        elif isinstance(value, dict):
            sum_value = sum(value.values())
        else:
            raise TypeError(value)
        if axis_width:
            detailed_caption_text = captions_for_axis.get(row_name) if captions_for_axis else None
            axis_label = self._get_axis_label(
                row_name, caption_text=detailed_caption_text,
                mark_size=mark_size, mark_style=mark_style,
            )
            caption_text = str(sum_value)
            detailed_caption = self._get_detailed_row_caption(detailed_caption_text or row_name)
            bar_style.display = 'inline-block'
        else:
            caption_text = f'{row_name}: {sum_value}'
            detailed_caption = None
            axis_label = None
        if captions_for_values:
            hint = f'{row_name}: {sum_value} {captions_for_values.get(row_name) or captions_for_axis.get(row_name, "")}'
        else:
            hint = f'{row_name}: {sum_value}'
        if isinstance(value, NUMERIC):
            bar = self._get_single_bar(
                value, scale_x=scale_x, bar_frame_size=bar_frame_size,
                bar_style=bar_style, caption=caption_text, hint=hint,
            )
        elif isinstance(value, dict):
            bar = self._get_multiple_bar(
                value, scale_x=scale_x, frame_size=bar_frame_size,
                style=bar_style, colors=colors, captions=captions_for_values, hint=hint,
            )
        else:
            raise TypeError(value)
        caption_width = row_frame_size.x - self.axis_width - bar.size.x
        if caption_width < 0:
            caption_width = Size1d(0)
        caption_size = Size2d(caption_width, bar_frame_size.y)
        caption = SquareView.horizontal(
            [f'{caption_text} {HTML_NB_SPACE}', detailed_caption],
            size=caption_size,
            style=Style(align_items='center', overflow_x='hidden', overflow_y='hidden'),
        )
        row = SquareView.horizontal([axis_label, bar, caption], size=row_frame_size, style=ROW_STYLE, hint=hint)
        assert isinstance(row, SquareView)
        return row

    @staticmethod
    def _get_single_bar(
            value: float,
            scale_x: Size1d,
            bar_frame_size: Size2d,
            bar_style: Style,
            caption: Optional[str] = None,
            hint: Optional[str] = None,
    ) -> SquareView:
        bar_width = scale_x * value
        if bar_width > bar_frame_size.x:
            bar_width = bar_frame_size.x
        bar_size = Size2d(bar_width, bar_frame_size.y)
        bar = SquareView(
            data=[caption],
            tag=TagType.Div,
            size=bar_size,
            style=bar_style,
            hint=hint,
        )
        return bar

    @classmethod
    def _get_multiple_bar(
            cls,
            values: OrderedDict,
            scale_x: Size1d,
            frame_size: Size2d,
            style: Style,
            colors: Optional[dict],
            captions: Optional[dict] = None,
            hint: Optional[str] = None,
    ) -> SquareView:
        sub_bars = list()
        for k, v in values.items():
            color = colors.get(k) if colors else None
            if color is None:
                color = cls._get_default_color_for_category(k)
            cur_style = style.modified(background=color)
            cur_caption = captions.get(k, k) if captions else k
            cur_caption = f'{v} {cur_caption}'
            cur_hint = f'{v}{HTML_NEW_LINE}{cur_caption}{HTML_NEW_LINE}{hint}'
            cur_bar = cls._get_single_bar(
                value=v,
                scale_x=scale_x,
                bar_frame_size=frame_size,
                bar_style=cur_style,
                caption=cur_caption,
                hint=cur_hint,
            )
            sub_bars.append(cur_bar)
        total_size = Size2d(x=scale_x*sum(values.values()), y=frame_size.y)
        multiple_bar = SquareView.horizontal(
            sub_bars,
            size=total_size,
            style=style,
            hint=hint,
        )
        return multiple_bar

    @staticmethod
    def _get_default_color_for_category(category: str, salt: str = '==') -> str:
        if category == 'total':
            return DEFAULT_CHART_COLOR
        elif category == 'other':
            return DEFAULT_BAR_COLOR
        else:
            num = crc32(bytes(salt + category, 'utf-8'))
            return '#' + hex(num)[-6:]

    @classmethod
    def _get_axis_label(
            cls,
            row_name: str,
            caption_text: Optional[str],
            mark_size: Size2d,
            mark_style: Style,
    ):
        if caption_text:
            row_hint = f'{row_name}{HTML_NEW_LINE}{caption_text}'
            detailed_caption = cls._get_detailed_row_caption(caption_text)
        else:
            row_hint = row_name
            detailed_caption = None
        axis_label = SquareView.vertical(
            data=[row_name, detailed_caption],
            size=mark_size,
            style=mark_style,
            hint=row_hint,
        )
        axis_label.style.display = 'inline-block'
        return axis_label

    @staticmethod
    def _get_detailed_row_caption(
            detailed_caption_text,
    ):
        caption_view = SquareView(
            detailed_caption_text,
            tag=TagType.Paragraph,
            style=DETAILED_CAPTION_STYLE,
            hint=detailed_caption_text,
        )
        return caption_view


class PairBarChartViewer(BarChartViewer):
    def __init__(
            self,
            size: Union[Size2d, Tuple[float, float]] = DEFAULT_CHART_SIZE,
            style: Optional[Style] = DEFAULT_CHART_STYLE,
            bar_style: str = DEFAULT_BAR_STYLE,
            scale_x: Optional[Size1d] = None,
            axis_width: Size1d = DEFAULT_AXIS_WIDTH,
            rel_bar_width: Size1d = DEFAULT_REL_BAR_WIDTH,
            max_depth: Optional[int] = None,
            padding: Optional[Size2d] = DEFAULT_PADDING,
    ):
        super().__init__(
            size=size, style=style, max_depth=max_depth,
            bar_style=bar_style, scale_x=scale_x, axis_width=axis_width, padding=padding,
        )
        self.rel_bar_width = rel_bar_width

    def get_view(
            self,
            obj: dict,
            include_title: bool = True,
            size: Optional[Size2d] = None,
            style: Optional[Style] = None,
            colors: Optional[dict] = None,
            depth: Optional[int] = None,
            prefix: Optional[FormattedView] = None,
            tag: Optional[TagType] = None,
            ordered: Optional[bool] = False,
            scale_x: Optional[Size1d] = None,
            bar_style: Style = DEFAULT_BAR_STYLE,
            padding: Optional[Size2d] = None,
            captions_for_axis: Optional[dict] = None,
            captions_for_values: Optional[dict] = None,
            axis_width: Optional[Size1d] = None,
            rel_bar_width: Optional[Size1d] = None,
    ) -> SquareView:
        if size is None:
            size = self.size
        if axis_width is None:
            axis_width = self.axis_width
        if rel_bar_width is None:
            rel_bar_width = self.rel_bar_width
        if style is None:
            style = self.style
        if scale_x is None:
            scale_x = self.scale_x
        if padding is None:
            padding = self.padding
        chart_size = size - padding * 2
        abs_chart_size = Size2d(chart_size.x - rel_bar_width, chart_size.y)
        rel_chart_size = Size2d(rel_bar_width, chart_size.y)
        rel_chart_view = self._get_chart_without_padding(
            self._get_rel_obj(obj), scale_x=rel_bar_width,
            chart_size=rel_chart_size, axis_width=None,
            style=style, bar_style=bar_style, colors=colors,
            captions_for_axis=captions_for_axis, captions_for_values=captions_for_values,
        )
        abs_chart_view = self._get_chart_without_padding(
            obj, scale_x=scale_x,
            chart_size=abs_chart_size, axis_width=axis_width,
            style=style, bar_style=bar_style, colors=colors,
            captions_for_axis=captions_for_axis, captions_for_values=captions_for_values,
            mark_style=MARK_STYLE.modified(text_align='center'),
        )
        chart_view = SquareView.horizontal(
            [rel_chart_view, abs_chart_view],
            size=chart_size,
            style=style,
        )
        chart_view = self._get_chart_with_padding(chart_view, padding=padding)
        return chart_view

    @staticmethod
    def _get_rel_obj(obj: OrderedDict[str, dict]) -> OrderedDict[str, dict]:
        rel_obj = OrderedDict()
        for bar_name, abs_series in obj.items():
            rel_series = OrderedDict()
            if isinstance(abs_series, NUMERIC):
                abs_series = OrderedDict(total=abs_series)
            assert isinstance(abs_series, dict), TypeError(abs_series)
            sum_value = sum(abs_series.values())
            for cat, abs_value in abs_series.items():
                rel_value = abs_value / sum_value
                rel_series[cat] = rel_value
            rel_obj[bar_name] = rel_series
        return rel_obj
