from typing import Iterable

from views.text_view import TextView


class FormattedView(TextView):
    def __init__(self, data):
        super().__init__(data=data)

    def get_md_lines(self):
        for line in self.get_text_lines():
            if isinstance(line, str):
                yield line
                yield '\n'
            elif hasattr(line, 'get_md_lines'):  # isinstance(line, ContentItem)
                yield from line.get_md_lines()
            elif isinstance(line, Iterable):
                yield from line
                yield '\n'
            else:
                raise ValueError

    def get_html_lines(self):
        for line in self.get_text_lines():
            if isinstance(line, str):
                yield f'<p>{line}</p>'
            elif hasattr(line, 'get_html_lines'):  # isinstance(line, ContentItem)
                yield from line.get_html_lines()
            elif isinstance(line, Iterable):
                yield '<p>'
                yield from line
                yield '</p>'
            else:
                raise ValueError
