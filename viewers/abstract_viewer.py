from abc import ABC

from interfaces.viewer_interface import ViewerInterface as Viewer
from abstract.common_abstract import CommonAbstract as Abstract
from wrappers.common_wrapper import CommonWrapper as Wrapper


class AbstractViewer(Abstract, Viewer, ABC):
    @staticmethod
    def _get_wrapped_object(obj) -> Wrapper:
        if not isinstance(obj, Wrapper):
            obj = Wrapper.wrap(obj)
        return obj

    def get_data(self, obj):
        if hasattr(obj, 'get_data'):
            return obj.get_data()
        else:
            return obj
