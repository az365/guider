from abc import ABC, abstractmethod


class ViewerInterface(ABC):

    @abstractmethod
    def get_view(self, obj):
        pass

    @abstractmethod
    def get_wrapped_object(self, obj):
        pass

    @abstractmethod
    def get_data(self, obj):
        pass
