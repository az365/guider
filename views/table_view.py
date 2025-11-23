from typing import Iterable, Iterator, Union, Optional

from util.types import Array
from util.functions import is_empty
from views.formatted_view import FormattedView

Native = FormattedView


class TableView(FormattedView):
    def __init__(self, data: Iterable[Array], columns: Optional[list] = None):
        super().__init__(data=data)
        self.columns = columns

    def has_struct(self) -> bool:
        return not is_empty(self.columns)

    def get_column_names(self) -> Optional[list]:
        if self.has_struct():
            return [str(c) for c in self.columns]

    def get_header(self) -> Optional[Native]:
        if self.has_struct():
            return TableView([self.get_column_names()])

    def get_body(self) -> Optional[Native]:
        return TableView(self.get_data())

    def get_iterable_rows(self, including_title: bool = False) -> Iterator[Iterable]:
        if including_title:
            yield self.get_column_names()
        for row in self.get_data():
            assert isinstance(row, Iterable)
            yield row

    def get_text_lines(self, including_title: bool = True) -> list:
        lines = list()
        for row in self.get_iterable_rows(including_title=including_title):
            if row is not None:
                row = ['-' if c is None else str(c) for c in row]
                line = '\t'.join(row)
                lines.append(line)
        return lines

    def get_md_lines(self) -> Iterator[str]:
        if self.has_struct():
            header = self.get_header()
            assert isinstance(header, TableView)
            yield from header.get_md_lines()
            line = ' | '.join(['---' for _ in self.get_column_names()])
            yield f'| {line} |'
        for row in self.get_iterable_rows(including_title=False):
            row = ['-' if c is None else str(c) for c in row]
            line = ' | '.join(row)
            yield f'| {line} |'

    def get_html_lines(self) -> Iterator[str]:
        yield '<table>'
        if self.has_struct():
            yield '<thead>'
            yield from self.get_header().get_html_rows()
            yield '</thead>'
        yield '<tbody>'
        yield from self.get_body().get_html_rows()
        yield '</tbody>'
        yield '</table>'

    def get_html_rows(self) -> Iterator[str]:
        for row in self.get_iterable_rows(including_title=False):
            assert isinstance(row, Iterable) and not isinstance(row, str)
            yield '<tr>'
            for cell in row:
                if isinstance(cell, FormattedView) or hasattr(cell, '_repr_html_'):
                    cell = cell._repr_html_()
                yield f'<td style="text-align: left;">{cell}</td>'
            yield '</tr>'
