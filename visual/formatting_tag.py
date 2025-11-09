from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Union

from util.functions import get_attr_str


class TagType(Enum):
    Paragraph = 'p'
    Header = 'h'
    HyperLink = 'a'
    List = 'ul'
    ListItem = 'li'
    Font = 'font'

    def get_class(self):
        if self.name == self.Paragraph.name:
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
    @abstractmethod
    def get_tag_type(self) -> TagType:
        pass

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

    def get_attributes(self, filled_only: bool = True) -> dict:
        if filled_only:
            attributes = dict()
            for k, v in vars(self).items():
                if v:
                    attributes[k] = v
            return attributes
        else:
            return vars(self)

    def get_html_attributes_str(self) -> str:
        attributes = self.get_attributes()
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


class Paragraph(AbstractFormattingTag):
    def get_tag_type(self) -> TagType:
        return TagType.Paragraph

    def get_md_open_tag(self) -> str:
        return '\n'

    def get_md_close_tag(self) -> str:
        return '\n'

    def get_text_open_tag(self) -> str:
        return '\n'


class Header(Paragraph):
    def __init__(self, level: int, name: Optional[str] = None):
        self.level = level
        self.name = name

    def get_tag_type(self) -> TagType:
        return TagType.Header

    def get_tag_name(self) -> str:
        return f'h{self.level}'

    def get_md_open_tag(self) -> str:
        return '#' * self.level + ' '

    def get_md_close_tag(self) -> str:
        if self.name:
            return ' {#' + self.name + '}'

    def get_attributes(self, filled_only: bool = True) -> dict:
        attributes = dict()
        if self.name or not filled_only:
            attributes['name'] = self.name
        return attributes

    def get_text_close_tag(self) -> str:
        return '\n====\n'


class HyperLink(AbstractFormattingTag):
    def __init__(self, href: str, name: str, title: str):
        self.href = href
        self.name = name
        self.title = title

    def get_tag_type(self) -> TagType:
        return TagType.HyperLink

    def get_md_open_tag(self) -> str:
        if self.href:
            return '['
        elif self.name:
            return f'[](#{self.name})\n'

    def get_md_close_tag(self) -> str:
        if self.href:
            if self.title:
                return f']({self.href} {self.title})'
            else:
                return f']({self.href})'

    def get_text_close_tag(self) -> str:
        return '[*]'


class List(AbstractFormattingTag):
    def __init__(self, ordered: bool = False):
        self.ordered = ordered

    def get_tag_type(self) -> TagType:
        return TagType.List

    def get_tag_name(self) -> str:
        if self.ordered:
            return 'ol'
        else:
            return 'ul'

    def get_attributes(self, filled_only: bool = True) -> dict:
        return dict()

    def get_md_open_tag(self) -> str:
        return '\n'

    def get_md_close_tag(self) -> str:
        return '\n'

    def get_text_open_tag(self) -> str:
        return '\n'

    def get_text_close_tag(self) -> str:
        return '\n'


class ListItem(AbstractFormattingTag):
    def __init__(self, ordered: bool = False):
        self.ordered = ordered

    def get_tag_type(self) -> TagType:
        return TagType.ListItem  # li

    def get_attributes(self, filled_only: bool = True) -> dict:
        return dict()

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
        if self._need_font_tag():
            tag += f'</font>'
        if self.bold:
            tag += '</b>'
        if self.italic:
            tag += '</i>'
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

    def get_attributes(self, filled_only: bool = True) -> dict:
        attributes = dict()
        if self.size or not filled_only:
            attributes['size'] = self.size
        if self.color or not filled_only:
            attributes['color'] = self.color
        return attributes

    def _need_font_tag(self) -> bool:
        if self.get_html_attributes_str():
            return True
        else:
            return False
