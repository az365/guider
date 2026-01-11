from collections import OrderedDict
from typing import Optional, Iterable, Union

from visual.size import Size2d
from visual.style import Style
from views.formatted_view import FormattedView, Tag, TagType

Native = FormattedView

DEFAULT_TAG_TYPE = TagType.Div


class SquareView(FormattedView):
    def __init__(
            self,
            data: Iterable,
            tag: Tag = DEFAULT_TAG_TYPE,
            size: Optional[Size2d] = None,
            style: Optional[Style] = None,
            hint: Optional[str] = None,
    ):
        super().__init__(data, tag or DEFAULT_TAG_TYPE)
        self.size = size if size is not None else Size2d(x=None, y=None)
        self.style = style or Style()
        self.set_hint(hint)

    @classmethod
    def horizontal(
            cls,
            data: Iterable,
            size: Optional[Size2d] = None,
            style: Optional[Style] = None,
            hint: Optional[str] = None,
    ) -> Native:
        style = Style(overflow_x='hidden').modified(style).modified(
            display='flex', flex_direction='row', flex_wrap='nowrap', white_space='nowrap',
        )
        view = cls(data=data, tag=TagType.Div, size=size, style=style, hint=hint)
        return view

    @classmethod
    def vertical(
            cls,
            data: Iterable,
            size: Optional[Size2d] = None,
            style: Optional[Style] = None,
            hint: Optional[str] = None,
    ) -> Native:
        style = Style(overflow_y='hidden').modified(style).modified(
            display='flex', flex_direction='column', flex_wrap='nowrap', white_space='normal',
        )
        view = cls(data=data, tag=TagType.Div, size=size, style=style, hint=hint)
        return view

    def get_hint(self) -> Optional[str]:
        return self.tag.hint

    def set_hint(self, text: Optional[str]):
        self.tag.hint = text

    hint = property(get_hint, set_hint)

    def get_html_open_tag(self) -> str:
        html_style = self.get_html_style_str()
        return self.tag.get_html_open_tag(style=html_style)

    def get_html_close_tag(self) -> str:
        tag_name = self.tag.get_tag_name()
        return f'</{tag_name}>'

    def get_html_width(self) -> Optional[str]:
        return self.size.get_html_width()

    def get_html_height(self) -> Optional[str]:
        return self.size.get_html_height()

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
