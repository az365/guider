from typing import Iterable, Sized, Optional
from collections import OrderedDict

from util.const import DEFAULT_LINE_LEN, REDUNDANT_SPACING
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


def remove_redundant_spacing(text: str) -> str:
    for double, single in REDUNDANT_SPACING.items():
        while double in text:
            text = text.replace(double, single)
    return text


def get_tech_name(obj):
    if hasattr(obj, 'tech_name'):
        return obj.tech_name
    elif hasattr(obj, 'get_tech_name'):
        return obj.get_tech_name()
    elif hasattr(obj, 'id'):
        return obj.id
    elif hasattr(obj, 'get_id'):
        return obj.get_id()
    elif hasattr(obj, 'get_name_or_str'):
        return obj.get_name_or_str()


def get_hint(obj, max_len: Optional[int] = None) -> str:
    if hasattr(obj, 'get_hint'):  # isinstance(obj, WrapperInterface)
        hint = obj.get_hint()
    elif isinstance(obj, dict):
        count = len(obj)
        columns = '2+' if isinstance(obj, OrderedDict) else '2'
        hint = f'{count}x{columns}'
    elif isinstance(obj, Sized) and not isinstance(obj, str):
        hint = f'{len(obj)}'
    else:
        hint = obj.__class__.__name__
    return crop(hint, max_len)


def get_repr(obj, max_len: Optional[int] = None) -> str:
    if isinstance(obj, PRIMITIVES):
        repr_str = repr(obj)
    elif hasattr(obj, 'get_repr'):  # isinstance(obj, WrapperInterface):
        repr_str = obj.get_repr()
    elif hasattr(obj, '__class__') and hasattr(obj, '__dict__'):
        cls = obj.__class__.__name__
        if max_len is None:
            max_attr_len = None
        else:
            max_attr_len = max_len - len(cls) - 2
        attr = get_attr_str(obj.__dict__, max_len=max_attr_len)
        repr_str = f'{cls}({attr})'
    else:
        repr_str = repr(obj)
    return crop(repr_str, max_len)


def get_array_str(
        obj: Iterable,
        scope: bool = False,
        quote: str = '',
        delimiter: str = ', ',
        max_len: Optional[int] = None,
) -> str:
    array = list()
    for i in obj:
        i_repr = get_tech_name(i)
        i_repr = str(i_repr or i)
        if quote:
            i_repr.replace(quote, '\\' + quote)
            i_repr = f'{quote}{i_repr}{quote}'
        else:
            i_repr = i_repr.replace(',', '\,')
        array.append(i_repr)
    array_str = delimiter.join(array)
    if scope:
        if max_len is not None:
            array_str = crop(array_str, max_len - 2)
        array_str = f'[{array_str}]'
    return crop(array_str, max_len)


def get_attr_str(obj: dict, quote: str = '', delimiter: str = ', ', max_len: Optional[int] = None) -> str:
    array = list()
    for k, v in obj.items():
        if quote:
            str(v).replace(quote, '\\' + quote)
            v = f'{quote}{v}{quote}'
        item = f'{k}={v}'
        array.append(item)
    return get_array_str(array, scope=False, quote='', delimiter=delimiter, max_len=max_len)


def crop(
        text,
        max_len: Optional[int] = DEFAULT_LINE_LEN,
        crop_suffix: str = '...',
        short_crop_suffix: str = '_',
) -> str:
    text = str(text)
    if max_len is not None:
        crop_len = len(crop_suffix)
        if max_len is not None:
            assert isinstance(max_len, int), TypeError('max_len bust be int or None')
            if max_len >= 0:
                text_len = len(text)
                if text_len > max_len:
                    value_len = max_len - crop_len
                    if value_len > 0:
                        text = text[:value_len] + crop_suffix
                    elif max_len > 1:
                        text = text[:max_len - 1] + short_crop_suffix
                    else:
                        text = text[:max_len]
            else:
                text = ''
    return text


def get_max_value(data: Iterable, sum_secondary: bool = False) -> float:
    max_value = None
    if isinstance(data, dict):
        data = data.values()
    for v in data:
        if isinstance(v, Iterable):
            if isinstance(v, dict):
                v = v.values()
            if sum_secondary:
                v = sum(v)
            else:
                v = max(v)
        if isinstance(v, (int, float)):
            if max_value is None:
                max_value = v
            elif v > max_value:
                max_value = v
        else:
            raise TypeError(v)
    return max_value


def smart_round(n: float, count: int = 2, upper: bool = False) -> float:
    if n >= 1 or n <= -1:
        num_digits = len(str(abs(int(n))))
    else:
        raise NotImplementedError
    round_digits = num_digits - count
    if upper:
        multiplier = 10 ** round_digits
        shift = 1 if n > 0 else -1
        rounded = (int(n / multiplier) + shift) * multiplier
    else:
        rounded = round(n, -round_digits)
    return rounded


def percentage(num: float, round_digits: Optional[int] = None, smart: bool = False, delimiter: str = '') -> str:
    num_percent = num * 100
    if round_digits is not None:
        if smart:
            num_percent = smart_round(num_percent, round_digits, upper=False)
        else:
            if round_digits:
                num_percent = round(num_percent, round_digits)
            if round_digits <= 0:
                num_percent = int(num_percent)
    return f'{num_percent}{delimiter}%'
