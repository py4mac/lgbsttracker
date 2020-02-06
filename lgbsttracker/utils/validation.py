from lgbsttracker.errors import ErrorCodes
from lgbsttracker.exceptions import GenericException
from lgbsttracker.store.db.db_types import DATABASE_ENGINES

_UNSUPPORTED_DB_TYPE_MSG = f"Supported database engines are {DATABASE_ENGINES}"


def _validate_db_type_string(db_type):
    """validates db_type parsed from DB URI is supported"""
    if db_type not in DATABASE_ENGINES:
        error_msg = "Invalid database engine: '%s'. '%s'" % (db_type, _UNSUPPORTED_DB_TYPE_MSG)
        raise GenericException(error_msg, ErrorCodes.INVALID_PARAMETER_VALUE)
