from collections import OrderedDict
from typing import Optional, Iterable, Union

from visual.size import Size2d
from visual.style import Style
from views.formatted_view import FormattedView, Tag, TagType

Native = FormattedView


class SquareView(FormattedView):
    def __init__(
            self,
            data: Iterable,
            tag: Tag = TagType.Div,
            size: Optional[Size2d] = None,
            style: Optional[Style] = None,
            hint: Optional[str] = None,
    ):
        super().__init__(data, tag)
        self.size = size or Size2d(x=None, y=None)
        self.style = style or Style()
        self.hint = hint

    @classmethod
    def horizontal(
            cls,
            data: Iterable,
            size: Size2d,
            style: Optional[Style] = None,
            hint: Optional[str] = None,
    ) -> Native:
        style = Style(overflow_x='hidden').modify(style).modify(
            display='flex', flex_direction='row', flex_wrap='nowrap', white_space='nowrap',
        )
        view = cls(data=data, tag=TagType.Div, size=size, style=style, hint=hint)
        return view

    @classmethod
    def vertical(
            cls,
            data: Iterable,
            size: Size2d,
            style: Optional[Style] = None,
            hint: Optional[str] = None,
    ) -> Native:
        style = Style(overflow_y='hidden').modify(style).modify(
            display='flex', flex_direction='column', flex_wrap='nowrap', white_space='normal',
        )
        view = cls(data=data, tag=TagType.Div, size=size, style=style, hint=hint)
        return view

    def get_html_open_tag(self) -> str:
        style = self.get_html_style_str()
        title = self.get_html_title()
        tag_name = self.tag.get_tag_name()
        if title:
            return f'<{tag_name} style="{style}" title="{title}">'
        else:
            return f'<{tag_name} style="{style}">'

    def get_html_close_tag(self) -> str:
        tag_name = self.tag.get_tag_name()
        return f'</{tag_name}>'

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
        style = self.style.get_html_dict()
        if self.get_html_width():
            style['width'] = self.get_html_width()
        if self.get_html_height():
            style['height'] = self.get_html_height()
        return style

    def __bool__(self):
        return bool(self.size)
