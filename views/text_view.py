from typing import Iterable, Optional

from util.functions import crop
from views.abstract_view import AbstractView

Native = AbstractView


class TextView(AbstractView):
    def __init__(self, data: Iterable[str]):
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

    data = property(get_data, set_data)

    def get_lines_count(self) -> int:
        return len(self.get_text_lines())

    def get_text_lines(self) -> list:
        return self.get_data()

    def get_text(self) -> str:
        return '\n'.join(self.get_text_lines())

    def _get_modified_view(self, data: Iterable, inplace: bool):
        if inplace:
            self.data = data
            return self
        else:
            return self.__class__(data)

    def crop(
            self,
            max_line_len: Optional[int],
            lines_count: Optional[int] = None,
            crop_suffix: str = '...',
            inplace: bool = True,
    ) -> Native:
        cropped_lines = self._get_cropped_lines(max_line_len, lines_count, crop_suffix=crop_suffix)
        return self._get_modified_view(cropped_lines, inplace=inplace)

    def _get_cropped_lines(
            self,
            max_line_len: Optional[int],
            lines_count: Optional[int] = None,
            crop_suffix: str = '...',
    ) -> Iterable[str]:
        for no, line in enumerate(self.get_text_lines()):
            if lines_count is not None and no < lines_count:
                if no + 1 == lines_count and self.get_lines_count() > lines_count:
                    line = crop_suffix
            if max_line_len is not None:
                line = crop(line, max_line_len)
            yield line

    def replace(self, __old: str, __new: str, inplace: bool = False) -> Native:
        """
        Return a copy with all occurrences of substring old replaced by new.
        """
        replaced_lines = self._get_replaced_lines(__old, __new)
        return self._get_modified_view(replaced_lines, inplace=inplace)

    def _get_replaced_lines(self, __old: str, __new: str) -> Iterable[str]:
        for line in self.get_text_lines():
            assert isinstance(line, str), TypeError(repr(line))
            yield line.replace(__old, __new)

    def get_repr(self):
        return repr(self.get_text())

    def __len__(self):
        return self.get_lines_count()

    def __str__(self):
        return self.get_text()

    def __repr__(self):
        return self.get_repr()
