from lgbsttracker.errors import ErrorCodeNames, ErrorCodes


class GenericException(Exception):
    """
    Generic exception thrown to surface failure information about external-facing operations.
    The error message associated with this exception may be exposed to clients in HTTP responses
    for debugging purposes. If the error text is sensitive, raise a generic `Exception` object
    instead.
    """

    def __init__(self, message, error_code=ErrorCodes.INTERNAL_ERROR, **kwargs):
        """
        :param message: The message describing the error that occured. This will be included in the
                        exception's serialized JSON representation.
        :param error_code: An appropriate error code for the error that occured; it will be included
                           in the exception's serialized JSON representation. This should be one of
                           the codes listed in the `lgbsttracker.errors.ErrorCodes`.
        :param kwargs: Additional key-value pairs to include in the serialized JSON representation
                       of the GenericException.
        """
        try:
            self.error_code = ErrorCodeNames.get(error_code)
        except (ValueError, TypeError):
            self.error_code = ErrorCodeNames.get(ErrorCodes.INTERNAL_ERROR)
        self.message = message
        self.json_kwargs = kwargs
        super(GenericException, self).__init__(message)


class DatabaseNotInitialized(GenericException):
    def __init__(self, message):
        super(DatabaseNotInitialized, self).__init__(message, error_code=ErrorCodes.INTERNAL_ERROR)
