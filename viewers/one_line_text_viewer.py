from typing import Iterable

from viewers.text_viewer import TextViewer


class OneLineTextViewer(TextViewer):
    def get_view(self, obj) -> str:
        data = self.get_data(obj)
        line = ''
        if isinstance(data, dict):
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
        return line
