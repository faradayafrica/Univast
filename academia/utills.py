# Third Party Imports
from rest_api_payload import success_response, error_response


def SuccessResponse(status, message, serializer):

    payload = success_response(
        status=status,
        message=message,
        data=serializer.data
    )
    
    return payload

def ErrorResponse(status, message):

    payload = error_response(
        status=status,
        message=message,
    )
    
    return payload