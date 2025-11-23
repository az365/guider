from collections.abc import Callable
from typing import Iterable

from util.functions import crop
from wrappers.common_wrapper import CommonWrapper
from viewers.text_viewer import TextViewer
from viewers.one_line_text_viewer import OneLineTextViewer
from views.text_view import TextView


class SimpleTextViewer(TextViewer):
    _get_one_line = OneLineTextViewer().get_view

    def get_view(self, obj, *args, **kwargs) -> TextView:
        lines = self.get_lines(obj, *args, **kwargs)
        return TextView(lines)

    def get_lines(self, obj, depth=1, indent='  ', max_line_len=80) -> Iterable[str]:
        if isinstance(obj, dict):
            for k, v in obj.items():
                wrapped_v = CommonWrapper(v)
                v_repr = wrapped_v.get_view(OneLineTextViewer())
                v_hint = wrapped_v.get_hint()
                if v_hint == 0:
                    yield f'{k} (0)'
                else:
                    yield f'{k} ({v_hint}): {v_repr}'
        elif isinstance(obj, Iterable) and not isinstance(obj, str):
            for k, v in enumerate(obj):
                v_repr = self._get_one_line(v)
                yield f'{k}: {v_repr}'
        elif isinstance(obj, Callable):  # Class
            yield from CommonWrapper(obj).get_view(OneLineTextViewer())
        else:
            yield self.get_title(obj)
            if depth > 0:
                obj = self.get_wrapped_object(obj)
                assert isinstance(obj, CommonWrapper)
                props = obj.get_props()
                for line in self.get_lines(props, depth=depth-1):
                    yield crop(indent + line, max_line_len)

    def get_blocks(self, obj, depth=1, indent='  ') -> Iterable[list]:
        for k, v in self.get_content_pairs(obj):
            block_lines = list()
            block_lines.append(k + ':')
            for line in self.get_lines(v, depth=depth - 1):
                block_lines.append(indent + line)
            yield block_lines

    def get_content_pairs(self, obj) -> Iterable[tuple]:
        obj = self.get_wrapped_object(obj)
        assert isinstance(obj, CommonWrapper)
        yield 'data', obj.get_data()
        yield 'props', obj.get_props()
        yield 'methods', obj.get_methods()
