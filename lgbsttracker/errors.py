class ErrorCodes:
    INTERNAL_ERROR = 0
    TEMPORARILY_UNAVAILABLE = 1
    ENDPOINT_NOT_FOUND = 2
    PERMISSION_DENIED = 3
    REQUEST_LIMIT_EXCEEDED = 4
    BAD_REQUEST = 5
    INVALID_PARAMETER_VALUE = 6
    RESOURCE_DOES_NOT_EXIST = 7
    INVALID_STATE = 8
    RESOURCE_ALREADY_EXISTS = 9


ErrorCodeNames = {
    ErrorCodes.INTERNAL_ERROR: "Internal Error",
    ErrorCodes.TEMPORARILY_UNAVAILABLE: "Temporarily Unavailable",
    ErrorCodes.ENDPOINT_NOT_FOUND: "Endpoint not found",
    ErrorCodes.PERMISSION_DENIED: "Permission denied",
    ErrorCodes.REQUEST_LIMIT_EXCEEDED: "Request limit exceeded",
    ErrorCodes.BAD_REQUEST: "Bad request",
    ErrorCodes.INVALID_PARAMETER_VALUE: "Invalid parameter value",
    ErrorCodes.RESOURCE_DOES_NOT_EXIST: "Resource does not exist",
    ErrorCodes.INVALID_STATE: "Invalid State",
    ErrorCodes.RESOURCE_ALREADY_EXISTS: "Resource already exists",
}
