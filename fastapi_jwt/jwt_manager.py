import jwt
from datetime import datetime, timedelta
from fastapi import Response, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, ValidationError
from functools import lru_cache
from jwt import ExpiredSignatureError
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Optional, Tuple, Dict

from pydantic import BaseSettings
from .handler import default_expired_token_response, default_required_token_response

class JWTConfig(BaseSettings):
    jwt_secret_key: str = None
    jwt_algorithm: str = None


class JWTManager(object):
    def __init__(self, app=None, settings=None):
        self.current_user = None
        if issubclass(settings.__class__, BaseSettings) is not True:
            raise ValueError('instance BaseSettings required')

        self.config = JWTConfig(
            jwt_secret_key = settings.jwt_secret_key,
            jwt_algorithm = settings.jwt_algorithm
        )

        self._expired_token_handler = default_expired_token_response
        self._required_token_handler = default_required_token_response
        if app is not None:
            self.init_app(app)

    @lru_cache()
    def get_jwt_config(self):
        return self.config

    def init_app(self, app):
        self._set_exception_handler(app)

    def _set_exception_handler(self, app):
        @app.exception_handler(ExpiredSignatureError)
        def handling_expired_error(e):
            return self._expired_token_handler(e)

    def expired_token_loader(self, callback):
        self._expired_token_handler = callback
        return callback


    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(data, self.config.jwt_secret_key, algorithm=self.config.jwt_algorithm)
        return encoded_jwt.decode('utf-8')

    def get_authorization_scheme_param(self, authorization_header_value: str) -> Tuple[str, str]:
        if not authorization_header_value:
            return "", ""
        scheme, _, param = authorization_header_value.partition(" ")
        return scheme, param

    def decode(self) -> Dict:
        try:
            if self.current_user is None:
                raise self._required_token_handler(None)
            payload = jwt.decode(self.current_user, self.config.jwt_secret_key, algorithms=self.config.jwt_algorithm)
            payload.pop('exp')
            return payload
        except jwt.exceptions.ExpiredSignatureError as e:
            raise self._expired_token_handler(e)
        except jwt.exceptions.DecodeError as e:
            raise self._expired_token_handler(e)

    def jwt_required(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        scheme, param = self.get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Not authenticated",
                    "status": 401
                },
                headers={"WWW-Authenticate": "Bearer"},
            )
        self.current_user = param
        self.decode()
        return self

    def get_jwt_identity(self):

        identity = self.decode()
        return identity

