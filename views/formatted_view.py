from typing import Optional, Iterable, Union

from util.ext import HTML, display
from util.const import INDENT
from util.types import PRIMITIVES
from visual import TagType, AbstractFormattingTag
from views.text_view import TextView

Native = TextView
Text = Union[TextView, str]
Tag = Union[AbstractFormattingTag, TagType, None]


class FormattedView(TextView):
    def __init__(self, data: Iterable[Text], tag: Tag = None):
        super().__init__(data=data)
        if isinstance(tag, TagType):
            tag = tag.create()
        assert isinstance(tag, AbstractFormattingTag) or tag is None
        self.tag = tag

    def get_tag_type(self) -> Optional[TagType]:
        if self.tag:
            assert isinstance(self.tag, AbstractFormattingTag), TypeError(self.tag)
            return self.tag.get_tag_type()

    def get_md_lines(self) -> Iterable[str]:
        one_line = ''.join(self._get_md_parts())
        yield from one_line.split('\n')

    def get_html_lines(self) -> Iterable[str]:
        if self.tag:
            open_tag, close_tag = self.get_html_open_tag(), self.get_html_close_tag()
            indent = INDENT
        else:
            open_tag, close_tag, indent = '', '', ''
        can_be_one_line = self.get_count() < 2
        if can_be_one_line:
            line = ''.join(self._get_html_parts())
            yield open_tag + line + close_tag
        else:
            if open_tag:
                yield open_tag
            for line in self._get_html_parts():
                yield indent + line
            if close_tag:
                yield close_tag

    def get_text_lines(self) -> Iterable[str]:
        one_line = ''.join(self._get_text_parts())
        one_line = one_line.replace('\n\n\n', '\n')
        one_line = one_line.replace('\n\n', '\n')
        yield from one_line.split('\n')

    def _get_text_parts(self) -> Iterable[str]:
        if self.tag:
            yield self.tag.get_text_open_tag()
        for i in self.get_data():
            if i is None:
                pass
            elif isinstance(i, str):
                yield i
            elif isinstance(i, PRIMITIVES):
                yield str(i)
            elif isinstance(i, FormattedView) or hasattr(i, '_get_text_parts'):
                if i.get_tag_type() == TagType.List:
                    for j in i._get_text_parts():
                        yield j.replace('\n', '\n' + INDENT)
                else:
                    yield from i._get_text_parts()
            elif isinstance(i, TextView):
                yield from i.get_text_lines()
            else:
                raise TypeError(i)
        if self.tag:
            yield self.tag.get_text_close_tag()

    def _get_md_parts(self):
        if self.tag:
            yield self.tag.get_md_open_tag()
        for i in self.get_data():
            if i is None:
                pass
            elif isinstance(i, str):
                yield i
            elif isinstance(i, FormattedView) or hasattr(i, '_get_md_parts'):
                if i.get_tag_type() == TagType.List:
                    for j in i._get_md_parts():
                        yield j.replace('\n', '\n' + INDENT)
                else:
                    yield from i._get_md_parts()
            elif isinstance(i, TextView):
                yield from i.get_text_lines()
            else:
                raise TypeError(i)
        if self.tag:
            yield self.tag.get_md_close_tag()

    def _get_html_parts(self):
        for i in self.get_data():
            if i is None:
                pass
            elif isinstance(i, str):
                yield i
            elif isinstance(i, PRIMITIVES):
                yield str(i)
            elif isinstance(i, FormattedView) or hasattr(i, 'get_html_lines'):
                yield from i.get_html_lines()
            elif isinstance(i, TextView):
                for line in self.get_text_lines():
                    yield f'{line}<br>'
            else:
                raise TypeError(repr(i))

    def get_html_open_tag(self) -> str:
        return self.tag.get_html_open_tag()

    def get_html_close_tag(self) -> str:
        return self.tag.get_html_close_tag()

    def show(self):
        if HTML:
            layout = HTML('\n'.join(self.get_html_lines()))
        else:
            layout = '\n'.join(self.get_text())
        return display(layout)

    def get_count(self):
        return len(self.get_data())

    def _repr_html_(self):
        return '\n'.join(self.get_html_lines())

    def _repr_markdown_(self):
        return '\n'.join(self.get_md_lines())
