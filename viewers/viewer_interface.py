from abc import ABC, abstractmethod


class ViewerInterface(ABC):

    @abstractmethod
    def get_view(self, obj):
        pass

    @staticmethod
    @abstractmethod
    def _get_wrapped_object(obj):
        pass

    @abstractmethod
    def get_data(self, obj):
        """
        Unwraps wrapped data from object.
        :param obj:
        :return: unwrapped data
        """
        pass
