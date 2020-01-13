from lgbsttracker.exceptions import LgbsttrackerException
from lgbsttracker.store.db.db_types import DATABASE_ENGINES
from lgbsttracker.protos.common_pb2 import INVALID_PARAMETER_VALUE

_UNSUPPORTED_DB_TYPE_MSG = "Supported database engines are {%s}" % ", ".join(DATABASE_ENGINES)


def _validate_db_type_string(db_type):
    """validates db_type parsed from DB URI is supported"""
    if db_type not in DATABASE_ENGINES:
        error_msg = "Invalid database engine: '%s'. '%s'" % (db_type, _UNSUPPORTED_DB_TYPE_MSG)
        raise LgbsttrackerException(error_msg, INVALID_PARAMETER_VALUE)
