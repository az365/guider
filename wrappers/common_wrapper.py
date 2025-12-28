from typing import Optional, Iterable, Union, Any
from collections import OrderedDict

from util.const import PATH_DELIMITER
from util.types import Class, PRIMITIVES, Array, ARRAY_TYPES
from util.functions import get_id, get_array_str, remove_empty_values_from_dict, crop, get_hint, get_repr
from abstract.common_abstract import CommonAbstract
from wrappers.wrapper_interface import WrapperInterface
from viewers.viewer_interface import ViewerInterface

Native = Union[CommonAbstract, WrapperInterface]

DEFAULT_PROPS = 'class', 'path'


class CommonWrapper(CommonAbstract, WrapperInterface):
    _default_viewer = None

    def __init__(self, obj, path: Optional[list] = None, root: Optional[WrapperInterface] = None):
        self._obj = obj
        self._path = path or []
        self._root = root  # empty root is self
        if hasattr(obj, 'short_name') and not path:
            self._path = [obj.short_name]

    def get_raw_object(self) -> Any:
        return self._obj

    def set_raw_object(self, obj):
        self._obj = obj

    obj = property(get_raw_object, set_raw_object)

    @staticmethod
    def _get_raw_object(obj):
        if isinstance(obj, CommonWrapper):
            return obj.get_raw_object()
        else:
            return obj

    def get_root(self) -> Native:
        if self._root:
            return self._root
        else:
            return self

    def get_path(self) -> list:
        return self._path

    def is_path_valid(self) -> bool:
        return self == self.get_root().get_node(self.get_path())

    def get_short_name(self) -> str:
        obj = self.get_raw_object()
        obj_id = get_id(obj)
        path = self.get_path()
        if obj_id:
            return obj_id
        elif path:
            return '.'.join(map(str, path))
        else:
            return str(self)

    def get_name_or_str(self) -> str:
        obj = self.get_raw_object()
        if isinstance(obj, PRIMITIVES):
            return str(obj)
        elif isinstance(obj, ARRAY_TYPES):
            return get_array_str(obj)
        elif hasattr(obj, 'get_name_or_str'):
            return obj.get_name_or_str()
        else:
            return self.get_short_name()

    @classmethod
    def wrap(cls, obj: Any, path: Optional[list] = None) -> Native:
        return CommonWrapper(obj, path=path)

    @classmethod
    def from_props(cls, props: dict, target_class: Class = dict, path: Optional[list] = None) -> Native:
        obj = target_class(**props)
        return cls.wrap(obj, path=path)

    @classmethod
    def set_default_viewer(cls, viewer: ViewerInterface):
        cls._default_viewer = viewer

    def get_data(self):
        obj = self.get_raw_object()
        if hasattr(obj, 'get_data'):
            return obj.get_data()
        else:
            return obj

    def get_class(self) -> Class:
        return self._obj.__class__

    def get_repr(self) -> str:
        obj = self.get_raw_object()
        obj_repr = get_repr(obj)
        return f'({obj_repr})'

    def get_hint(self) -> str:
        obj = self.get_raw_object()
        hint = get_hint(obj)
        return f'({hint})'

    def get_vars(self, including_protected: bool = False) -> dict:
        obj = self.get_raw_object()
        if isinstance(obj, dict):
            return obj
        elif isinstance(obj, ARRAY_TYPES):
            props = dict()
            for n, i in enumerate(obj):
                props[n] = i
            return props
        if hasattr(obj, '__dict__'):
            if including_protected:
                return vars(obj)
            else:
                props = dict()
                for k, v in vars(obj).items():
                    if k[0] != '_':
                        props[k] = v
            return props
        else:
            return dict(data=obj)

    def get_props(
            self,
            including_protected: bool = False,
            add: Optional[Iterable] = None,
            skip_empty: bool = False,
    ) -> OrderedDict:
        obj = self.get_raw_object()
        props = OrderedDict()
        if add is None:
            add = [] if isinstance(obj, dict) else DEFAULT_PROPS
        for i in add:
            props[i] = self.get_property(i)

        if hasattr(obj, 'get_props'):  # isinstance(obj, Entity)
            if isinstance(obj, CommonWrapper):
                props.update(obj.get_props(add=[]))
            else:
                props.update(obj.get_props())
        elif isinstance(obj, dict):
            props.update(obj)
        elif isinstance(obj, ARRAY_TYPES):
            for n, i in enumerate(obj):
                props[n] = i
        elif hasattr(obj, '__dict__'):
            for i in self.get_raw_property_names(including_protected=including_protected):
                props[i] = getattr(obj, i)
        else:
            props['data'] = obj

        if skip_empty:
            props = remove_empty_values_from_dict(props)
        return props

    def get_serializable_props(
            self,
            depth: Optional[int] = None,
            use_ids: bool = False,
            skip_empty: bool = False,
            ordered: bool = True,
    ):
        obj = self.get_raw_object()
        if isinstance(obj, PRIMITIVES):  # bool, int, float, str
            return obj
        if isinstance(obj, type):
            return repr(obj)
        if depth == 0:
            return self.get_name_or_str()
        if not isinstance(obj, ARRAY_TYPES + (set, dict)):
            obj = self.get_props(including_protected=False, add=['class'], skip_empty=skip_empty)
        return self._get_serializable(
            obj,
            depth=depth,
            use_ids=use_ids,
            skip_empty=skip_empty,
            ordered=ordered,
        )

    def _get_serializable(
            self,
            obj: Iterable,
            depth: Optional[int] = None,
            use_ids: bool = False,
            skip_empty: bool = False,
            ordered: bool = True,
    ):
        if isinstance(obj, dict):
            serializable_props = OrderedDict() if ordered else dict()
            items = obj.items()
            is_list = False
        elif isinstance(obj, ARRAY_TYPES + (set, )):
            serializable_props = list()
            is_list = True
            items = enumerate(obj)
        else:
            raise TypeError(f'expected dict or array, got {obj} as {type(obj)}')

        for k, v in items:
            v_id = get_id(v) if use_ids else None
            if v_id is not None:
                v_serializable = v_id
            else:
                if not isinstance(v, CommonWrapper):
                    v = CommonWrapper.wrap(v, path=self.get_path() + [k])
                v_depth = depth - 1 if depth is not None else None
                v_serializable = v.get_serializable_props(
                    depth=v_depth,
                    use_ids=use_ids,
                    skip_empty=skip_empty,
                    ordered=ordered,
                )
            if is_list:
                serializable_props.append(v_serializable)
            else:  # is dict
                serializable_props[k] = v_serializable
        if is_list:
            if not isinstance(obj, (list, set)):  # list is default, set is not serializable
                cls = obj.__class__
                serializable_props = cls(serializable_props)
        return serializable_props

    def get_methods(self, including_protected: bool = False) -> dict:
        obj = self.get_raw_object()
        methods = dict()
        for name in self.get_method_names(including_protected):
            value = getattr(obj, name)
            methods[name] = value
        return methods

    def get_attributes(self, including_protected: bool = False) -> dict:
        attributes = dict()
        obj = self.get_raw_object()
        for key in self.get_attribute_names(including_protected):
            value = getattr(obj, key)
            attributes[key] = value
        return attributes

    def get_attribute_names(self, including_protected: bool = False) -> Iterable[str]:
        obj = self.get_raw_object()
        try:
            names = obj.__dir__()
        except TypeError:  # obj is Class
            names = tuple()
        if including_protected:
            return names
        else:
            for n in names:
                if not n.startswith('_'):
                    yield n

    def get_raw_property_names(self, including_protected: bool = False) -> list:
        obj = self.get_raw_object()
        property_names = list()
        if hasattr(obj, '__dict__'):
            if including_protected:
                property_names += vars(obj).keys()
            else:
                for i in vars(obj):
                    if not i.startswith('_'):
                        property_names.append(i)
        for i in self.get_attribute_names(including_protected=including_protected):
            if hasattr(obj.__class__, i):
                attr = getattr(obj.__class__, i)
                if isinstance(attr, property):
                    property_names.append(i)
        return property_names

    def get_method_names(self, including_protected: bool = False) -> Iterable[str]:
        prop_names = self.get_props(add=[]).keys()
        for name in self.get_attribute_names(including_protected):
            if name not in prop_names:
                yield name

    def get_raw_property(self, name: str):
        obj = self.get_raw_object()
        if isinstance(obj, dict):
            if name in obj:
                return obj[name]
        elif isinstance(obj, ARRAY_TYPES):
            if isinstance(name, str):
                if name.isnumeric():
                    name = int(name)
            if isinstance(name, int):
                return obj[name]
            else:
                for i in obj:
                    if hasattr(i, 'short_name'):
                        if i.short_name == name:
                            return i
                    wrapped_i = CommonWrapper(i)
                    if hasattr(wrapped_i, 'get_name'):
                        if wrapped_i.get_name() == name:
                            return i
        if name == 'data' and not hasattr(obj, 'data'):
            return obj
        elif [name] == self.get_path():
            return obj
        else:
            if hasattr(obj, name):
                return getattr(obj, name)
            elif hasattr(obj, f'get_{name}'):
                method = getattr(obj, f'get_{name}')
                return method()
            elif hasattr(self, name):
                return getattr(self, name)
            elif hasattr(self, f'get_{name}'):
                method = getattr(self, f'get_{name}')
                return method()
            else:
                props = self.get_props(add=[])
                if name in props:
                    return props[name]
                else:
                    available_keys_str = ', '.join(map(str, props.keys()))
                    raise ValueError(f'{name} not found (available: {available_keys_str})')

    def get_wrapped_property(self, name: str):
        prop = self.get_raw_property(name)
        if isinstance(prop, CommonWrapper):
            return prop
        else:
            path = self.get_path() + [name]
            root = self.get_root()
            return CommonWrapper(prop, path=path, root=root)

    def get_property(self, name: str, wrapped: bool = True):
        if wrapped:
            return self.get_wrapped_property(name)
        else:
            return self.get_raw_property(name)

    def get_node(self, path: Union[Array, str], wrapped: bool = True):
        if not path:
            return self
        elif isinstance(path, str):
            path = path.split(PATH_DELIMITER)
        path_len = len(path)
        if path_len == 0:
            return self
        elif path_len == 1:
            return self.get_property(path[0], wrapped=wrapped)
        else:
            prop = self.get_property(path[0], wrapped=True)
            assert isinstance(prop, CommonWrapper)
            return prop.get_node(path[1:], wrapped=wrapped)

    def get_props_str(self, max_len: int = 50) -> str:
        obj = self.get_raw_object()
        if isinstance(obj, str):
            props_list = [obj]
        elif isinstance(obj, ARRAY_TYPES):
            props_list = [repr(i) for i in obj]
        elif not (isinstance(obj, dict) or hasattr(obj, '__dict__')):
            props_list = [repr(obj)]
        else:
            props_list = [f'{k}={v}' for k, v in self.get_props(add=[]).items()]
        line = ', '.join(props_list)
        return crop(line, max_len)

    def __str__(self):
        cls = self.__class__.__name__
        obj = self.get_raw_object()
        return f'{cls}({obj})'

    def __eq__(self, other):
        raw_self = self.get_raw_object()
        raw_other = self._get_raw_object(other)
        return raw_self == raw_other

    def get_view(self, viewer: Optional[ViewerInterface] = None):
        if not viewer:
            viewer = self._default_viewer
        if not viewer:
            raise ValueError('viewer not set')
        return viewer.get_view(self)

    def print(self, viewer: Optional[ViewerInterface] = None):
        if not viewer:
            viewer = self._default_viewer
        if not viewer:
            raise ValueError('viewer not set')
        if hasattr(viewer, 'print'):
            viewer.print(self)
        else:
            raise TypeError(f'provided viewer must be an instance of TextViewer, got {viewer}')
