from abc import ABC, abstractmethod

from interfaces.default_interface import DefaultInterface as Default
from interfaces.view_interface import ViewInterface as View


class ViewerInterface(Default, ABC):
    """
    Используется для создания представлений (отображений) объектов (обёрнутых CommonWrapper или совместимым враппером).
    Хранит настройки отображения объектов, использует их в создаваемых View.
    """

    @abstractmethod
    def get_view(self, obj) -> View:
        """
        Returns a prepared view of provided object.
        :param obj: object to represent in view.
        :return: view as an object of ViewInterface.
        """
        pass

    @abstractmethod
    def _get_data_from(self, obj):
        """
        Unwraps wrapped data from object.
        :param obj:
        :return: unwrapped data
        """
        pass
