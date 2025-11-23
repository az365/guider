from viewers.viewer_interface import ViewerInterface
from wrappers.common_wrapper import CommonWrapper


class AbstractViewer(ViewerInterface):
    def __init__(self):
        pass

    def get_view(self, obj):
        pass

    @staticmethod
    def _get_wrapped_object(obj) -> CommonWrapper:
        if not isinstance(obj, CommonWrapper):
            obj = CommonWrapper.wrap(obj)
        return obj

    def get_data(self, obj):
        if hasattr(obj, 'get_data'):
            return obj.get_data()
        else:
            return obj

    def __repr__(self):
        cls = self.__class__.__name__
        kwarg_str_list = []
        for k, v in self.__dict__.items():
            kwarg_str_list.append(f'{k}={v}')
        kwarg_str = ', '.join(kwarg_str_list)
        return f'{cls}({kwarg_str})'

    def __str__(self):
        return self.__repr__()
