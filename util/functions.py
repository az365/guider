from typing import Iterable, Sized
from collections import OrderedDict

from util.const import DEFAULT_LINE_LEN
from util.types import PRIMITIVES


def is_empty(obj) -> bool:
    if obj is None:
        return True
    elif hasattr(obj, '__len__'):
        if len(obj) == 0:
            return True
    return False


def remove_empty_values_from_dict(input_dict: dict, inplace: bool = False) -> dict:
    if inplace:
        empty_keys = set()
        for k, v in input_dict.items():
            if is_empty(v):
                empty_keys.add(k)
        for i in empty_keys:
            input_dict.pop(i)
        return input_dict
    else:
        output_dict = input_dict.__class__()  # supports OrderedDict
        for k, v in input_dict.items():
            if not is_empty(v):
                output_dict[k] = v
        return output_dict


def get_id(obj):
    if hasattr(obj, 'id'):
        return obj.id
    elif hasattr(obj, 'get_id'):
        return obj.get_id()
    elif hasattr(obj, 'short_name'):
        return obj.short_name
    elif hasattr(obj, 'get_short_name'):
        return obj.get_name_or_str()


def get_hint(obj) -> str:
    if hasattr(obj, 'get_hint'):  # isinstance(obj, WrapperInterface)
        return obj.get_hint()
    elif isinstance(obj, dict):
        count = len(obj)
        columns = '2+' if isinstance(obj, OrderedDict) else '2'
        return f'{count}x{columns}'
    elif isinstance(obj, Sized) and not isinstance(obj, str):
        return f'{len(obj)}'
    else:
        return obj.__class__.__name__


def get_repr(obj) -> str:
    if isinstance(obj, PRIMITIVES):
        return repr(obj)
    elif hasattr(obj, 'get_repr'):  # isinstance(obj, WrapperInterface):
        return obj.get_repr()
    elif hasattr(obj, '__class__') and hasattr(obj, '__dict__'):
        cls = obj.__class__.__name__
        attr = get_attr_str(obj.__dict__)
        return f'{cls}({attr})'
    else:
        return repr(obj)


def get_array_str(obj: Iterable, scope: bool = False, quote: str = '', delimiter: str = ', ') -> str:
    array = list()
    for i in obj:
        i_repr = get_id(i)
        i_repr = str(i_repr or i)
        if quote:
            i_repr.replace(quote, '\\' + quote)
            i_repr = f'{quote}{i_repr}{quote}'
        else:
            i_repr = i_repr.replace(',', '\,')
        array.append(i_repr)
    array_str = delimiter.join(array)
    if scope:
        return f'[{array_str}]'
    else:
        return array_str

def get_attr_str(obj: dict, quote: str = '', delimiter: str = ', ') -> str:
    array = list()
    for k, v in obj.items():
        if quote:
            str(v).replace(quote, '\\' + quote)
            v = f'{quote}{v}{quote}'
        item = f'{k}={v}'
        array.append(item)
    return get_array_str(array, scope=False, quote='', delimiter=delimiter)

def crop(
        text,
        max_len: int = DEFAULT_LINE_LEN,
        crop_suffix: str = '...',
        short_crop_suffix: str = '_',
) -> str:
    text = str(text)
    crop_len = len(crop_suffix)
    if max_len is not None:
        assert isinstance(max_len, int), TypeError('max_len bust be int or None')
        text_len = len(text)
        if text_len > max_len:
            value_len = max_len - crop_len
            if value_len > 0:
                text = text[:value_len] + crop_suffix
            elif max_len > 1:
                text = text[:max_len - 1] + short_crop_suffix
            else:
                text = text[:max_len]
    return text
