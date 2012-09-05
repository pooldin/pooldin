def to_bool(value):
    if value in ['True', 'true', '1']:
        return True

    if value in ['False', 'false', '0']:
        return False

    return bool(value)


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
