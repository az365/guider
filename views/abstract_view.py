from util.functions import get_repr
from abstract.common_abstract import CommonAbstract


class AbstractView(CommonAbstract):
    def __init__(self, data):
        self._data = None
        self.set_data(data)

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    data = property(get_data, set_data)

    def get_repr(self):
        obj_repr = get_repr(self.get_data())
        return f'({obj_repr})'

    def __str__(self):
        return str(self.get_data())

    def __iter__(self):
        yield from self.get_data()

    def __len__(self):
        return len(self.get_data())

    def __bool__(self):
        return bool(self.get_data())

    def __add__(self, other):
        return self.__class__([self, other])
