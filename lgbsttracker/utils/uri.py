from six.moves import urllib

from lgbsttracker.errors import ErrorCodes
from lgbsttracker.exceptions import GenericException
from lgbsttracker.store.db.db_types import DATABASE_ENGINES
from lgbsttracker.utils.validation import _validate_db_type_string

_INVALID_DB_URI_MSG = "Please refer to format specifications."


def extract_db_type_from_uri(db_uri):
    """
    Parse the specified DB URI to extract the database type. Confirm the database type is
    supported. If a driver is specified, confirm it passes a plausible regex.
    """
    scheme = urllib.parse.urlparse(db_uri).scheme
    scheme_plus_count = scheme.count("+")

    if scheme_plus_count == 0:
        db_type = scheme
    elif scheme_plus_count == 1:
        db_type, _ = scheme.split("+")
    else:
        error_msg = "Invalid database URI: '%s'. %s" % (db_uri, _INVALID_DB_URI_MSG)
        raise GenericException(error_msg, ErrorCodes.INVALID_PARAMETER_VALUE)

    _validate_db_type_string(db_type)

    return db_type


def get_uri_scheme(uri_or_path):
    scheme = urllib.parse.urlparse(uri_or_path).scheme
    if any([scheme.lower().startswith(db) for db in DATABASE_ENGINES]):
        return extract_db_type_from_uri(uri_or_path)
    else:
        return scheme


def extract_host_name_from_uri(uri_or_path):
    return urllib.parse.urlparse(uri_or_path).hostname
