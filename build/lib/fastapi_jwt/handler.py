from fastapi import Response
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

def default_expired_token_response(expired_token):
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Token has expired"
        }
    )

def default_required_token_response(token):
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Required Token"
        }
    )