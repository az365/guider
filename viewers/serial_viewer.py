from typing import Optional

from views.serial_view import SerialView
from viewers.abstract_viewer import AbstractViewer


class SerialViewer(AbstractViewer):
    def __init__(self, depth: Optional[int] = None, use_tech_names: bool = False, skip_empty: bool = False):
        super().__init__()
        self.depth = depth
        self.use_tech_names = use_tech_names
        self.skip_empty = skip_empty

    def get_view(self, obj):
        obj = self._get_wrapped_object(obj)
        return SerialView(obj, depth=self.depth, use_tech_names=self.use_tech_names, skip_empty=self.skip_empty)

    @staticmethod
    def get_view_class():
        return SerialView

    def parse(self, line: str, serial_format: str ='yaml', *args, **kwargs):
        parser = getattr(self.get_view_class(), f'parse_{serial_format}')
        return parser(line, *args, **kwargs)
