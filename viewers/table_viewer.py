from typing import Sized, Optional, Iterable, Callable, Union

from viewers.tree_viewer import TreeViewer
from views.table_view import TableView
from viewers.text_viewer import TextViewer
from viewers.one_line_text_viewer import OneLineTextViewer


class TableViewer(TextViewer):
    _get_one_line = OneLineTextViewer().get_view
    _get_list_view = TreeViewer(depth=1).get_view

    def __init__(self, depth: bool = False):
        super().__init__()
        self.depth = depth

    def get_view(
            self,
            obj,
            depth: Optional[bool] = None,
    ) -> TableView:
        if depth is None:
            depth = self.depth
        if depth:
            cell_getter = self._get_list_view
        else:
            cell_getter = self._get_one_line
        if isinstance(obj, (tuple, list, set)) and not isinstance(obj, str):
            records = list(self._get_table_records_from_iter(obj, cell_getter))
            columns = list(self._get_columns_from_records(records))
            rows = list(self._get_rows_from_records(records, columns))
        elif isinstance(obj, dict):
            columns = 'field', 'hint', 'value'
            rows = list(self._get_table_rows_from_dict(obj, cell_getter))
        else:
            obj = self.get_wrapped_object(obj)
            props = obj.get_props()
            return self.get_view(props, depth=depth)
        return TableView(data=rows, columns=columns)

    def _get_table_records_from_iter(self, obj: Iterable, cell_getter: Optional[Callable] = None) -> Iterable[dict]:
        if not cell_getter:
            cell_getter = self._get_one_line
        for i in obj:
            yield {
                k: cell_getter(v)
                for k, v in
                self.get_wrapped_object(i).get_props().items()
            }

    def _get_table_rows_from_dict(self, obj: dict, cell_getter: Optional[Callable] = None) -> Iterable[dict]:
        if not cell_getter:
            cell_getter = self._get_one_line
        for field, value in obj.items():
            if isinstance(value, dict):
                hint = f'({len(value)}x2)'
            elif isinstance(value, Sized):
                hint = f'({len(value)})'
            else:
                hint = value.__class__.__name__
            value_repr = cell_getter(value)
            yield field, hint, value_repr

    @staticmethod
    def _get_columns_from_records(records: Iterable[dict]) -> list:
        columns = list()
        for r in records:
            for field in r:
                if field not in columns:
                    columns.append(field)
        return columns

    @staticmethod
    def _get_rows_from_records(records: Iterable[dict], columns: Union[list, tuple]) -> Iterable[tuple]:
        for rec in records:
            row = [rec.get(c) for c in columns]
            yield tuple(row)
