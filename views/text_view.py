from typing import Iterable

from views.abstract_view import AbstractView


class TextView(AbstractView):
    def __init__(self, data):
        super().__init__(data)

    def get_data(self) -> list:
        return self._data

    def set_data(self, data):
        if isinstance(data, str):
            data = data.split('\n')
        elif isinstance(data, list):
            pass
        elif isinstance(data, Iterable):
            data = list(data)
        else:
            data = str(data).split('\n')
        self._data = data

    def get_text_lines(self) -> list:
        return self.get_data()

    def get_text(self) -> str:
        return '\n'.join(self.get_text_lines())

    def __str__(self):
        return self.get_text()

    def __repr__(self):
        return repr(self.get_text())
