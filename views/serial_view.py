from typing import Optional
import json

from views.abstract_view import AbstractView
from wrappers.common_wrapper import CommonWrapper


class SerialView(AbstractView):
    def __init__(self, data, depth: Optional[int] = None, use_ids: bool = False, skip_empty: bool = False):
        super().__init__(data)
        self.depth = depth
        self.use_ids = use_ids
        self.skip_empty = skip_empty

    def get_json(self) -> str:
        data = self.get_data()
        if not isinstance(data, CommonWrapper):
            data = CommonWrapper.wrap(data)
        serializable_props = data.get_serializable_props(self.depth, use_ids=self.use_ids, skip_empty=self.skip_empty)
        return json.dumps(serializable_props, ensure_ascii=False)

    def get_yaml(self) -> str:
        raise NotImplemented
