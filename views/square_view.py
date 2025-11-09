from collections import OrderedDict
from typing import Optional, Iterable, Union

from visual.size import Size
from visual.style import Style
from views.formatted_view import FormattedView


class SquareView(FormattedView):
    def __init__(self, data: Iterable, tag, size: Size, style: Style, hint: str):
        super().__init__(data, tag)
        self.size = size
        self.style = style or Style()
        self.hint = hint  # ToDo: or move to FormattingTag ?

    def get_html_lines(self) -> Iterable[str]:
        yield self.get_html_open_tag()
        yield from super().get_html_lines()
        yield self.get_html_close_tag()

    def get_html_open_tag(self) -> str:
        style = self.get_html_style_str()
        title = self.get_html_title()
        if title:
            return f'<div style="{style}" title="{title}">'
        else:
            return f'<div style="{style}">'

    def get_html_close_tag(self) -> str:
        return '</div>'

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
        style = self.style._get_html_style_dict()
        if self.get_html_width():
            style['width'] = self.get_html_width()
        if self.get_html_height():
            style['height'] = self.get_html_height()
        return style
