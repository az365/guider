from typing import Iterable

from util.types import PRIMITIVES
from views.text_view import TextView
from viewers.text_viewer import TextViewer


class OneLineTextViewer(TextViewer):
    def get_view(self, obj) -> TextView:
        data = self.get_data(obj)
        line = ''
        if isinstance(data, str):
            line = data
        elif isinstance(data, PRIMITIVES):
            line = str(data)
        elif isinstance(data, TextView):
            line = data.get_text()
        elif isinstance(data, dict):
            for k, v in data.items():
                if line:
                    line += ', '
                line += f'{k}: {v}'
        elif isinstance(data, Iterable) and not isinstance(data, str):  ###
            for i in data:
                if line:
                    line += ', '
                line += repr(i)
        elif isinstance(data, type):  # class
            line = data.__name__
        elif callable(data):  # method or function
            if hasattr(data, '__name__'):
                name = data.__name__
                try:
                    method = data
                    parent = method.__reduce__()[1][0]
                    cls = parent.__class__.__name__
                    line = f'{cls}.{name}()'
                except TypeError or AttributeError:
                    line = f'{name}()'
            else:
                line = 'lambda-function'
        elif hasattr(data, '__name__'):
            name = data.__name__
            line = name
        else:
            line = str(data)
        return TextView([line])
