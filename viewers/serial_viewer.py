from views.serial_view import SerialView
from viewers.abstract_viewer import AbstractViewer


class SerialViewer(AbstractViewer):
    def __init__(self):
        super().__init__()

    def get_view(self, obj):
        obj = self.get_wrapped_object(obj)
        return SerialView(obj)
