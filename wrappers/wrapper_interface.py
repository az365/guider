from typing import Optional, Iterable, Union, Any

from util.types import Array
from viewers.viewer_interface import ViewerInterface


class WrapperInterface:
    def get_raw_object(self) -> Any:
        pass

    @classmethod
    def wrap(cls, obj: Any):
        pass

    @classmethod
    def set_default_viewer(cls, viewer: ViewerInterface):
        pass

    def get_hint(self) -> str:
        pass

    def get_props(self, including_protected: bool = False) -> dict:
        pass

    def get_methods(self, including_protected: bool = False) -> dict:
        pass

    def get_attributes(self, including_protected: bool = False) -> dict:
        pass

    def get_attribute_names(self, including_protected: bool = False) -> Iterable[str]:
        pass

    def get_method_names(self, including_protected: bool = False) -> Iterable[str]:
        pass

    def get_property(self, name: str, wrapped: bool = True):
        pass

    def get_node(self, path: Union[Array, str], wrapped: bool = True):
        pass

    def get_view(self, viewer: Optional[ViewerInterface] = None):
        pass

    def print(self, viewer: Optional[ViewerInterface] = None) -> None:
        pass
