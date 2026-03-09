from abc import ABC, abstractmethod
from typing import Any

Native = Any


class DefaultInterface(ABC):
    """
    Common interface for all main classes of this project.
    """

    @abstractmethod
    def copy(self) -> Native:
        pass

    @abstractmethod
    def modified(self, other: Native = None, **kwargs) -> Native:
        pass
