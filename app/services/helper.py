import datetime

# JSON success response
def successResponse(responseMessage, responseResult, responseCode):
    response = {
        'success' : True,
        'message' : responseMessage,
        'result'  : responseResult,
        'serverdatetime' : datetime.datetime.now(),
        'db_version' : '1.0',
        'http_code' : responseCode
    }
    return response

# JSON failure response
def failureResponse(errorMessage, errorResult, responseCode):
    response = {
        'success' : False,
        'message' : errorMessage,
        'result' : errorResult,
        'http_code' : responseCode
    }
    
    return response