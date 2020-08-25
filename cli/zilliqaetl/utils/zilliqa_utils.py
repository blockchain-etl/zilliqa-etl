def to_int(val):
    if val is None:
        return val
    if isinstance(val, str):
        return int(val)

    return val
