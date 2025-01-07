from viewers.abstract_viewer import AbstractViewer
from views.text_view import TextView


class TextViewer(AbstractViewer):
    def get_view(self, obj) -> TextView:
        obj = self.get_wrapped_object(obj)
        return TextView(obj)

    def get_title(self, obj) -> str:
        obj = self.get_wrapped_object(obj)
        obj2 = obj.get_raw_object()
        cls = obj2.__class__.__name__
        name = repr(obj2)
        return f'{cls} {name}'

    def print(self, obj):
        view = self.get_view(obj)
        print(view)
