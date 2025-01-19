from typing import Optional
import json
import yaml

from views.abstract_view import AbstractView
from wrappers.common_wrapper import CommonWrapper


class IndentDumper(yaml.SafeDumper):
    # increase indent according Ansible style: https://habr.com/ru/articles/669684/
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, indentless=False)


class SerialView(AbstractView):
    def __init__(self, data, depth: Optional[int] = None, use_ids: bool = False, skip_empty: bool = False):
        super().__init__(data)
        self.depth = depth
        self.use_ids = use_ids
        self.skip_empty = skip_empty

    def get_serializable_props(self, ordered: bool = True):
        data = self.get_data()
        if not isinstance(data, CommonWrapper):
            data = CommonWrapper.wrap(data)
        return data.get_serializable_props(
            self.depth,
            use_ids=self.use_ids,
            skip_empty=self.skip_empty,
            ordered=ordered,
        )

    def get_json(self) -> str:
        data = self.get_serializable_props(ordered=True)
        return json.dumps(data, ensure_ascii=False)

    def get_yaml(self) -> str:
        data = self.get_serializable_props(ordered=False)
        return yaml.dump(data, Dumper=IndentDumper, allow_unicode=True)
