class AbstractView:
    def __init__(self, data):
        self._data = None
        self.set_data(data)

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    data = property(get_data, set_data)

    def __repr__(self):
        return repr(self._data)

    def __str__(self):
        return str(self._data)
