from abc import ABC, abstractmethod
from typing import Optional, Union, Any

from util.types import Array
from interfaces.default_interface import DefaultInterface as Default
from interfaces.view_interface import ViewInterface as View
from interfaces.viewer_interface import ViewerInterface as Viewer

Native = Default


class WrapperInterface(Default, ABC):
    """
    A family of wrapper-classes providing common interface for any python-objects of any classes.
    Used for their unified processing, conversion, and visualization.
    """

    @abstractmethod
    def get_raw_object(self) -> Any:
        """
        Returns raw wrapped object.
        :return: raw wrapped object.
        """
        pass

    @classmethod
    @abstractmethod
    def wrap(cls, obj: Any) -> Native:
        """
        Class method returns wrapped object as an instance of wrapper-class.
        :param obj: any python object to wrap.
        :return: wrapped object as an instance of wrapper-class.
        """
        pass

    @classmethod
    @abstractmethod
    def set_default_viewer(cls, viewer: Viewer):
        """
        Class method sets default viewer for methods .get_view() and print() of this wrapper-class.
        :param viewer: selected instance of viewer-classes implementing ViewerInterface.
        :return: wrapped object as an instance of wrapper-class.
        """
        pass

    @abstractmethod
    def get_hint(self) -> str:
        """
        Returns small text representation of wrapped object for icons and HTML-popups.
        :return: small text representation of wrapped object for icons and HTML-popups.
        """
        pass

    @abstractmethod
    def get_props(self, including_protected: bool = False) -> dict:
        """
        Returns mapping of available properties from wrapped objects.
        :param including_protected: boolean option regulating displaying of protected attributes (default is False).
        :return: mapping of available properties from wrapped objects (as dictionary).
        """
        pass

    @abstractmethod
    def get_serializable_props(
            self,
            depth: Optional[int] = None,
            use_tech_names: bool = False,
            skip_empty: bool = False,
            ordered: bool = True,
    ):
        """
        Converts values from wrapped object to serializable equivalents.
        Used for converting to YAML, JSON and other serialized formats.
        :param depth: max depth of recursion (disabled by default).
        :param use_tech_names: return tech-names (ids or paths) of other wrapped objects instead of their full values.
        :param skip_empty: do not return properties with non-filled values (None, default).
        :param ordered: ...
        :return: serializable python objects.
        """
        pass

    @abstractmethod
    def get_methods(self, including_protected: bool = False) -> dict:
        """
        Returns mapping of available methods from wrapped objects.
        :param including_protected: boolean option regulating displaying of protected attributes (default is False).
        :return: mapping of available methods from wrapped objects (as dictionary).
        """
        pass

    @abstractmethod
    def get_attributes(self, including_protected: bool = False) -> dict:
        """
        Returns mapping of available attributes from wrapped objects.
        :param including_protected: boolean option regulating displaying of protected attributes (default is False).
        :return: mapping of available attributes from wrapped objects (as dictionary).
        """
        pass

    @abstractmethod
    def get_property(self, name: str, wrapped: bool = True) -> Any:
        """
        Returns value of selected property from wrapped object.
        :param name: selected property name.
        :param wrapped: boolean option to wrap property value.
        :return: value of selected property from wrapped object.
        """
        pass

    @abstractmethod
    def get_node(self, path: Union[Array, str], wrapped: bool = True) -> Any:
        """
        Returns value of selected property from wrapped object,
        like get_property() but recursively including nested objects and their properties.
        :param path: sequence of selected property names.
        :param wrapped: boolean option to wrap property value.
        :return: value of selected property from wrapped object.
        """
        pass

    @abstractmethod
    def get_view(self, viewer: Optional[Viewer] = None) -> View:
        """
        Returns some text or visual representation of wrapped object.
        :param viewer: selected viewer.
        :return: text or visual representation of wrapped object.
        """
        pass

    @abstractmethod
    def print(self, viewer: Optional[Viewer] = None) -> None:
        pass
