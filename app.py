from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from jwt import ExpiredSignatureError
from fastapi_jwt.jwt_manager import JWTManager
from fastapi.exceptions import ValidationError, HTTPException



from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    jwt_secret_key: str = "SECRET_KEY"
    jwt_algorithm: str = "HS256"

settings = Settings()

app = FastAPI()

jwt = JWTManager(app, settings)

@app.post("/")
def read_root():
    identity = jwt.get_jwt_identity()
    return {"data": identity}


@app.post('/login')
def login():
    data = {
        "username":"restureese"
    }
    token = jwt.create_access_token(data)
    return JSONResponse(
        status_code=HTTP_200_OK,
        content={
            "access_token":token
        }
    )