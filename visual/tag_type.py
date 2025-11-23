from enum import Enum

tag_classes = None


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
        if tag_classes is None:
            raise ImportError('formatting_tag module must be imported before TagType.get_class() usage')
        else:
            assert isinstance(tag_classes, dict), TypeError(tag_classes)
        cls = tag_classes.get(self.name)
        if cls is None:
            raise ValueError(f'class for {self} not defined')
        else:
            return cls

    def get_builder(self):
        cls = self.get_class()
        if hasattr(cls, 'create'):
            return cls.create
        else:
            return cls

    def create(self, *args, **kwargs):
        builder = self.get_builder()
        return builder(*args, **kwargs)

    @staticmethod
    def set_classes(**kwargs):
        global tag_classes
        tag_classes = kwargs


PARAGRAPH_LIKE_TAGS = TagType.Paragraph, TagType.Header, TagType.ListItem
PARAGRAPH_PART_TAGS = TagType.HyperLink, TagType.Font
TEXT_LINE_TAGS = *PARAGRAPH_LIKE_TAGS, *PARAGRAPH_PART_TAGS
CANNOT_BE_ONE_LINE_TAGS = TagType.ListItem,
