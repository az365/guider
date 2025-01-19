from typing import Optional, Iterable, Callable, Union, Type, Any
from collections import OrderedDict

from wrappers.wrapper_interface import WrapperInterface, Array, ARRAY_TYPES, PATH_DELIMITER
from viewers.viewer_interface import ViewerInterface

Class = Union[Type, Callable]

DEFAULT_PROPS = 'class', 'path'
PRIMITIVES = bool, int, float, str


class CommonWrapper(WrapperInterface):
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

    def get_root(self) -> WrapperInterface:
        if self._root:
            return self._root
        else:
            return self

    def get_path(self) -> list:
        return self._path

    def is_path_valid(self) -> bool:
        return self == self.get_root().get_node(self.get_path())

    @classmethod
    def wrap(cls, obj: Any, path: Optional[list] = None):
        return CommonWrapper(obj, path=path)

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

    def get_hint(self) -> Union[str, int]:
        obj = self.get_raw_object()
        if isinstance(obj, CommonWrapper):
            return obj.get_hint()
        elif isinstance(obj, (list, tuple, set)):
            return len(obj)
        elif isinstance(obj, dict):
            count = len(list)
            columns = '2+' if isinstance(obj, OrderedDict) else '2'
            return f'{count}*{columns}'
        else:
            return type(obj).__name__

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

    def get_props(self, including_protected: bool = False, add: Optional[Iterable] = None) -> dict:
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
        return props

    def get_serializable_props(self, depth: Optional[int] = None, use_ids: bool = False, skip_empty: bool = False):
        serializable_props = OrderedDict()
        obj = self.get_raw_object()
        if isinstance(obj, PRIMITIVES):
            serializable_props = obj
        elif isinstance(obj, ARRAY_TYPES):
            serializable_props = list()
            for n, i in enumerate(obj):
                i_id = self._get_id(i) if use_ids else None
                if i_id is not None:
                    i_serializable = i_id
                else:
                    if not isinstance(i, CommonWrapper):
                        i = CommonWrapper.wrap(i, path=self.get_path() + [n])
                    if depth == 0:
                        i_serializable = str(i)
                    else:
                        i_depth = depth - 1 if depth is not None else None
                        i_serializable = i.get_serializable_props(depth=i_depth, use_ids=use_ids, skip_empty=skip_empty)
                serializable_props.append(i_serializable)
            serializable_props = obj.__class__(serializable_props)
        elif isinstance(obj, type):
            serializable_props = repr(type)
        elif depth == 0:
            serializable_props = str(obj)
        else:
            props = self.get_props(including_protected=False, add=['class'])
            for k, v in props.items():
                skip_v = False
                v_id = self._get_id(v) if use_ids else None
                if v_id is not None:
                    v_serializable = v_id
                else:
                    if skip_empty:
                        if v is None:
                            skip_v = True
                        elif hasattr(v, '__len__'):
                            if len(v) == 0:
                                skip_v = True
                    if skip_v:
                        v_serializable = None
                    else:
                        if not isinstance(v, CommonWrapper):
                            v = CommonWrapper.wrap(v, path=self.get_path() + [k])
                        v_depth = depth - 1 if depth is not None else None
                        v_serializable = v.get_serializable_props(depth=v_depth, use_ids=use_ids, skip_empty=skip_empty)
                if not skip_v:
                    serializable_props[k] = v_serializable
        return serializable_props

    @staticmethod
    def _get_id(obj):
        if hasattr(obj, 'id'):
            return obj.id
        elif hasattr(obj, 'get_id'):
            return obj.get_id()
        elif hasattr(obj, 'short_name'):
            return obj.short_name

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
            value = obj.__getattr__(key)
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
        if len(line) > max_len:
            line = line[:max_len - 3] + '...'
        return line

    def __str__(self):
        cls = self.__class__.__name__
        obj = self.get_raw_object()
        return f'{cls}({obj})'

    def __repr__(self):
        cls = self.__class__.__name__
        props = repr(self.get_raw_object())
        return f'{cls}({props})'

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
