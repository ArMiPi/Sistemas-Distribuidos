from __future__ import annotations

import datetime
import hashlib
from typing import TYPE_CHECKING

import grpc
from typing_extensions import Literal

import auth_pb2
import auth_pb2_grpc

if TYPE_CHECKING:
    from auth_pb2 import AuthResponse, LoginRequest, RegisterRequest

SECRET_KEY = "mysecret"


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self):
        self.__users: dict[str, dict[Literal["username", "password"], str]] = {}

    def Register(self, request: RegisterRequest, context) -> AuthResponse:
        token = self.__generate_token(request.username)

        if token in self.__users:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Username already exists")
            return auth_pb2.AuthResponse()

        password_hash = hashlib.sha256(request.password.encode()).hexdigest()

        self.__users.update(
            {token: {"username": request.username, "password": password_hash}}
        )

        return auth_pb2.AuthResponse(token=token)

    def Login(self, request: LoginRequest, context) -> AuthResponse:
        token = self.__generate_token(request.username)
        password_hash = hashlib.sha256(request.password.encode()).hexdigest()

        user_info = self.__users.get(token)

        if not user_info or user_info["password"] != password_hash:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid username or password")
            return auth_pb2.AuthResponse()

        return auth_pb2.AuthResponse(token=token)

    def __generate_token(self, username: str) -> str:
        hash_object = hashlib.sha256()
        hash_object.update(username.encode("utf-8"))

        return hash_object.hexdigest()
