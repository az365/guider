from abc import ABC, abstractmethod

from interfaces.default_interface import DefaultInterface


class ViewInterface(DefaultInterface, ABC):
    """
    A family of classes for storing partially prepared data for display.
    It can convert prepared data to some formats, can parse some of these formats.

    For example, SerialView stores hierarchical structures,
    and can send/receive JSON, YAML (XML may be added later).
    FormattedView and TableView can provide MarkDown, HTML,
    FormattedView stores rows (or similar objects),
    TableView stores arrays of table rows represented as arrays of cells.
    """

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def set_data(self, data):
        pass

    data = property(get_data, set_data)
