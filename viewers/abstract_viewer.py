from util.functions import get_repr
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
        return get_repr(self)

    def __str__(self):
        return self.__repr__()
