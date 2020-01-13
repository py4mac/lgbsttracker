from datetime import datetime


def parse_date(text):
    """
    Date parser format.
        Supported formats:
            "%Y-%m-%d"
            "%Y-%m-%dT%H:%M:%S"
            "%Y-%m-%d %H:%M:%S"

    :param text: Date text input string

    :return: :py:class:`datetime'
    """
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H-%M-%S"):
        try:
            return datetime.strptime(text, fmt)
        except Exception:
            pass
    raise None


def datetime_to_string(date, fmt="%Y-%m-%dT%H-%M-%S"):
    """ Convert date to string in format.

    :param :py:class:`datetime' date object
    :param fmt: Datetime format

    :return: string corresponding to the format
    """
    try:
        return date.strftime(fmt)
    except Exception:
        return ""


def datetime_to_seconds(dt):
    """ Convert datetime to seconds.

    :param :py:class:`datetime' dt object

    :return: int number of seconds from 01/01/1970
    """
    return int((dt - datetime(1970, 1, 1)).total_seconds())
