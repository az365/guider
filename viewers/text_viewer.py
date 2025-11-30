from util.functions import get_repr
from views.text_view import TextView
from viewers.abstract_viewer import AbstractViewer


class TextViewer(AbstractViewer):
    def get_view(self, obj) -> TextView:
        obj = self._get_wrapped_object(obj)
        return TextView(obj)

    def get_title(self, obj) -> str:
        obj = self._get_wrapped_object(obj)
        raw_obj = obj.get_raw_object()
        cls = raw_obj.__class__.__name__
        name = get_repr(raw_obj)
        return f'{cls} {name}'

    def print(self, obj):
        view = self.get_view(obj)
        print(view)
