import json

from views.abstract_view import AbstractView
from wrappers.common_wrapper import CommonWrapper


class SerialView(AbstractView):
    def __init__(self, data):
        super().__init__(data)

    def get_json(self) -> str:
        data = self.get_data()
        if not isinstance(data, CommonWrapper):
            data = CommonWrapper.wrap(data)
        serializable_props = data.get_serializable_props()
        return json.dumps(serializable_props)

    def get_yaml(self) -> str:
        raise NotImplemented
