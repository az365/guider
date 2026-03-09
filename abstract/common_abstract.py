from abc import ABC

from util.functions import get_repr
from interfaces.default_interface import DefaultInterface

Native = DefaultInterface


class CommonAbstract(DefaultInterface, ABC):
    def _get_init_kwargs(self, skip_none: bool = True) -> dict:
        init_kwargs = dict()
        for k, v in vars(self).items():
            if v is not None or not skip_none:
                if k.startswith('_'):
                    k = k[1:]
                init_kwargs[k] = v
        return init_kwargs

    def copy(self) -> Native:
        init_kwargs = self._get_init_kwargs(skip_none=True)
        return self.__class__(**init_kwargs)

    def modified(self, other: Native = None, **kwargs) -> Native:
        init_kwargs = self._get_init_kwargs(skip_none=True)
        if other:
            assert isinstance(other, self.__class__), TypeError(other)
            init_kwargs.update(other._get_init_kwargs())
        init_kwargs.update(kwargs)
        return self.__class__(**init_kwargs)

    def __repr__(self):
        return get_repr(self)

    def __str__(self):
        return repr(self)
