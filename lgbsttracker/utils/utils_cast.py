def cast(val, type_dest, default_value=None):
    """ Convert val value into type_dest with default_value in case of exception.

    :param val: Input Value
    :param type_dest: Type destination
    :param default_value: Default Value

    :return: input val cast
    """
    try:
        return type_dest(val)
    except Exception:
        return default_value
