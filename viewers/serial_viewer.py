from typing import Optional

from views.serial_view import SerialView
from viewers.abstract_viewer import AbstractViewer


class SerialViewer(AbstractViewer):
    def __init__(self, depth: Optional[int] = None, use_ids: bool = False, skip_empty: bool = False):
        super().__init__()
        self.depth = depth
        self.use_ids = use_ids
        self.skip_empty = skip_empty

    def get_view(self, obj):
        obj = self.get_wrapped_object(obj)
        return SerialView(obj, depth=self.depth, use_ids=self.use_ids, skip_empty=self.skip_empty)
