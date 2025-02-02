from typing import Iterable


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


def get_array_str(obj: Iterable, scope: bool = False, quote: str = '') -> str:
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
    array_str = ', '.join(array)
    if scope:
        return f'[{array_str}]'
    else:
        return array_str
