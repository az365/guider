def is_empty(obj) -> bool:
    if obj is None:
        return True
    elif hasattr(obj, '__len__'):
        if len(obj) == 0:
            return True
    return False


def get_id(obj):
    if hasattr(obj, 'id'):
        return obj.id
    elif hasattr(obj, 'get_id'):
        return obj.get_id()
    elif hasattr(obj, 'short_name'):
        return obj.short_name
    elif hasattr(obj, 'get_short_name'):
        return obj.get_name_or_str()
