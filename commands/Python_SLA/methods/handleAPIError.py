def handle_api_error(status_code):
    error_messages = {
        400: "Bad request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Data not found",
        405: "Method not allowed",
        415: "Unsupported media type",
        429: "Rate limit exceeded",
        500: "Internal server error",
        502: "Bad gateway",
        503: "Service unavailable",
        504: "Gateway timeout",
    }

    if status_code in error_messages:
        raise Exception({"code":status_code,"message":error_messages[status_code]})
    else:
        raise Exception({"code":status_code,"message":f'Unknown error with status code: {status_code}'})