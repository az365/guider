from viewers.viewer_interface import ViewerInterface
from wrappers.common_wrapper import CommonWrapper


class AbstractViewer(ViewerInterface):
    def __init__(self):
        pass

    def get_view(self, obj):
        pass

    def get_wrapped_object(self, obj):
        if not isinstance(obj, CommonWrapper):
            obj = CommonWrapper(obj)
        return obj

    def get_data(self, obj):
        if hasattr(obj, 'get_data'):
            return obj.get_data()
        else:
            return obj
