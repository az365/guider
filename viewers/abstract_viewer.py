from abstract.common_abstract import CommonAbstract
from viewers.viewer_interface import ViewerInterface
from wrappers.common_wrapper import CommonWrapper


class AbstractViewer(CommonAbstract, ViewerInterface):
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
