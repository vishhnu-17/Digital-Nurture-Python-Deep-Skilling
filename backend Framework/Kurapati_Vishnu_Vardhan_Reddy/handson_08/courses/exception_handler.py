from rest_framework.views import exception_handler
def custom_exception_handler(exception,context):
    response=exception_handler(exception,context)
    if response is None:
        return response
    error_code=None
    message=""
    field=None
    if response.status_code==404:
        error_code="NOT_FOUND"
    elif response.status_code==400:
        error_code="BAD_REQUEST"
    elif response.status_code==401:
        error_code="UNAUTHORIZED"
    elif response.status_code==403:
        error_code="FORBIDDEN" 
    elif response.status_code==405:
        error_code="METHOD_NOT_ALLOWED"     
    elif response.status_code==500:
        error_code="INTERNAL_SERVER_ERROR"
    if isinstance(response.data,dict):
        if "detail" in response.data:
            message=response.data["detail"]
        else:
            first_field=next(iter(response.data))
            field=first_field
            value=response.data[first_field]
            
            if isinstance(value,list):
                message=value[0]
            else:
                message=value
    else:
        message=str(response.data)
    response.data={
        "error":{
            "code":error_code,
            "message":str(message),
            "field": field
        }
    } 
    return response                                 
        
            
    