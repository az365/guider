from abc import ABC, abstractmethod
from typing import Optional, Iterable, Union, Any

from util.types import Array
from viewers.viewer_interface import ViewerInterface


class WrapperInterface(ABC):
    @abstractmethod
    def get_raw_object(self) -> Any:
        pass

    @classmethod
    @abstractmethod
    def wrap(cls, obj: Any):
        pass

    @classmethod
    @abstractmethod
    def set_default_viewer(cls, viewer: ViewerInterface):
        pass

    @abstractmethod
    def get_hint(self) -> str:
        pass

    @abstractmethod
    def get_props(self, including_protected: bool = False) -> dict:
        pass

    @abstractmethod
    def get_methods(self, including_protected: bool = False) -> dict:
        pass

    @abstractmethod
    def get_attributes(self, including_protected: bool = False) -> dict:
        pass

    @abstractmethod
    def get_attribute_names(self, including_protected: bool = False) -> Iterable[str]:
        pass

    @abstractmethod
    def get_method_names(self, including_protected: bool = False) -> Iterable[str]:
        pass

    @abstractmethod
    def get_property(self, name: str, wrapped: bool = True):
        pass

    @abstractmethod
    def get_node(self, path: Union[Array, str], wrapped: bool = True):
        pass

    @abstractmethod
    def get_view(self, viewer: Optional[ViewerInterface] = None):
        pass

    @abstractmethod
    def print(self, viewer: Optional[ViewerInterface] = None) -> None:
        pass
