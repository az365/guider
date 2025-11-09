from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Union

from util.functions import get_attr_str

HTML_ATTR_MAPPING = dict(id='name', title='hint', href='url')


class TagType(Enum):
    Div = 'div'
    Span = 'span'
    Paragraph = 'p'
    Header = 'h'
    HyperLink = 'a'
    List = 'ul'
    ListItem = 'li'
    Font = 'font'

    def get_class(self):
        if self.name == self.Div.name:
            return Div
        elif self.name == self.Span.name:
            return Span
        elif self.name == self.Paragraph.name:
            return Paragraph
        elif self.name == self.Header.name:
            return Header
        elif self.name == self.HyperLink.name:
            return HyperLink
        elif self.name == self.List.name:
            return List
        elif self.name == self.ListItem.name:
            return ListItem
        elif self.name == self.Font.name:
            return Font
        else:
            raise ValueError

    def get_builder(self):
        cls = self.get_class()
        if hasattr(cls, 'create'):
            return cls.create
        else:
            return cls

    def create(self, *args, **kwargs):
        builder = self.get_builder()
        return builder(*args, **kwargs)


class AbstractFormattingTag(ABC):
    def __init__(self, name: Optional[str] = None, hint: Optional[str] = None, style: Optional[str] = None):
        self.name = name
        self.hint = hint
        self.style = style

    @abstractmethod
    def get_tag_type(self) -> TagType:
        pass

    @classmethod
    def _get_html_excluded_attributes(cls) -> list:
        return list()

    def get_tag_name(self) -> str:
        return self.get_tag_type().value

    def get_html_open_tag(self) -> str:
        tag_name = self.get_tag_name()
        attributes = self.get_html_attributes_str()
        if attributes:
            return f'<{tag_name} {attributes}>'
        else:
            return f'<{tag_name}>'

    def get_html_close_tag(self) -> str:
        tag_name = self.get_tag_name()
        return f'</{tag_name}>'

    def get_attributes(self, filled_only: bool = True, exclude: Optional[list] = None) -> dict:
        attributes = dict()
        for k, v in vars(self).items():
            take = True
            if filled_only:
                take = take and v is not None
            if exclude:
                take = take and k not in exclude
            if take:
                attributes[k] = v
        return attributes

    def get_html_attributes_str(self) -> str:
        excluding = self._get_html_excluded_attributes()
        attributes = self.get_attributes(filled_only=True, exclude=excluding)
        for html_name, default_name in HTML_ATTR_MAPPING.items():
            if default_name in attributes:
                attributes[html_name] = attributes.pop(default_name)
        return get_attr_str(attributes, delimiter=' ', quote='"')

    @abstractmethod
    def get_md_open_tag(self) -> str:
        pass

    @abstractmethod
    def get_md_close_tag(self) -> str:
        pass

    def get_text_open_tag(self) -> str:
        return ''

    def get_text_close_tag(self) -> str:
        return ''


class Div(AbstractFormattingTag):
    def get_tag_type(self) -> TagType:
        return TagType.Div

    def get_md_open_tag(self) -> str:
        return '\n'

    def get_md_close_tag(self) -> str:
        return '\n'

    def get_text_open_tag(self) -> str:
        return '\n'


class Span(Div):
    def get_tag_type(self) -> TagType:
        return TagType.Span


class Paragraph(Span):
    def get_tag_type(self) -> TagType:
        return TagType.Paragraph


class Header(Paragraph):
    def __init__(
            self,
            level: int,
            name: Optional[str] = None, hint: Optional[str] = None, style: Optional[str] = None,
    ):
        super().__init__(name=name, hint=hint, style=style)
        self.level = level

    def get_tag_type(self) -> TagType:
        return TagType.Header

    def get_tag_name(self) -> str:
        return f'h{self.level}'

    def get_md_open_tag(self) -> str:
        return '#' * self.level + ' '

    def get_md_close_tag(self) -> str:
        if self.name:
            return ' {#' + self.name + '}'

    @classmethod
    def _get_html_excluded_attributes(cls) -> list:
        excluded = super()._get_html_excluded_attributes()
        excluded.append('level')
        return excluded

    def get_text_close_tag(self) -> str:
        return '\n====\n'


class HyperLink(AbstractFormattingTag):
    def __init__(
            self,
            url: str,
            name: Optional[str] = None, hint: Optional[str] = None, style: Optional[str] = None,
    ):
        super().__init__(name=name, hint=hint, style=style)
        self.url = url

    def get_tag_type(self) -> TagType:
        return TagType.HyperLink

    def get_md_open_tag(self) -> str:
        if self.url:
            return '['
        elif self.name:
            return f'[](#{self.name})\n'

    def get_md_close_tag(self) -> str:
        if self.url:
            if self.hint:
                return f']({self.url} {self.hint})'
            else:
                return f']({self.url})'

    def get_text_close_tag(self) -> str:
        return '[*]'


class List(AbstractFormattingTag):
    def __init__(
            self,
            ordered: bool = False,
            name: Optional[str] = None, hint: Optional[str] = None, style: Optional[str] = None,
    ):
        super().__init__(name=name, hint=hint, style=style)
        self.ordered = ordered

    def get_tag_type(self) -> TagType:
        return TagType.List

    def get_tag_name(self) -> str:
        if self.ordered:
            return 'ol'
        else:
            return 'ul'

    @classmethod
    def _get_html_excluded_attributes(cls) -> list:
        excluded = super()._get_html_excluded_attributes()
        excluded.append('ordered')
        return excluded

    def get_md_open_tag(self) -> str:
        return '\n'

    def get_md_close_tag(self) -> str:
        return '\n'

    def get_text_open_tag(self) -> str:
        return '\n'

    def get_text_close_tag(self) -> str:
        return '\n'


class ListItem(AbstractFormattingTag):
    def __init__(
            self,
            ordered: bool = False,
            name: Optional[str] = None, hint: Optional[str] = None, style: Optional[str] = None,
    ):
        super().__init__(name=name, hint=hint, style=style)
        self.ordered = ordered

    def get_tag_type(self) -> TagType:
        return TagType.ListItem  # li

    @classmethod
    def _get_html_excluded_attributes(cls) -> list:
        excluded = super()._get_html_excluded_attributes()
        excluded.append('ordered')
        return excluded

    def get_md_open_tag(self) -> str:
        if self.ordered:
            return '1. '
        else:
            return '- '

    def get_md_close_tag(self) -> str:
        return '\n'

    def get_text_open_tag(self) -> str:
        return '\n- '


class Font(AbstractFormattingTag):
    def __init__(
            self,
            size: Union[int, str, None] = None,
            color: Optional[str] = None,
            bold: Optional[bool] = None,
            italic: Optional[bool] = None,
            name: Optional[str] = None, hint: Optional[str] = None, style: Optional[str] = None,
    ):
        self.size = size
        self.color = color
        self.bold = bold
        self.italic = italic

    def get_tag_type(self) -> TagType:
        return TagType.Font

    def get_html_open_tag(self) -> str:
        tag = ''
        if self._need_font_tag():
            attributes = self.get_html_attributes_str()
            tag += f'<font {attributes}>'
        if self.bold:
            tag += '<b>'
        if self.italic:
            tag += '<i>'
        return tag

    def get_html_close_tag(self) -> str:
        tag = ''
        if self.italic:
            tag += '</i>'
        if self.bold:
            tag += '</b>'
        if self._need_font_tag():
            tag += f'</font>'
        return tag

    def get_md_open_tag(self) -> str:
        tag = ''
        if self.bold:
            tag += '**'
        if self.italic:
            tag += '*'
        return tag

    def get_md_close_tag(self) -> str:
        tag = ''
        if self.bold:
            tag += '**'
        if self.italic:
            tag += '*'
        return tag

    def get_text_open_tag(self) -> str:
        return ''

    def get_text_close_tag(self) -> str:
        return ''

    @classmethod
    def _get_html_excluded_attributes(cls) -> list:
        excluded = super()._get_html_excluded_attributes()
        excluded += ['bold', 'italic']
        return excluded

    def _need_font_tag(self) -> bool:
        if self.get_html_attributes_str():
            return True
        else:
            return False
