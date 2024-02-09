import base64
import socket
from typing import TypedDict


class SMTPOptions(TypedDict):
    username: str
    password: str




class SMTPClient:
    def __init__(self, host: str, port: int, options: SMTPOptions) -> None:
        self.host: str = host
        self.port: int = port
        self.options = options

    def __del__(self):
        self.close()

    def connect(self) -> None:
        self.__connection = socket.create_connection((self.host, self.port))
        response = repr(self.__connection.recv(1024))
        code = response[2:5]
        if code != "220":
            raise RuntimeError(f"Couldn't connect to {self.host} at port {self.port}")

    def __send(self, data: bytes):
        data = data + b"\r\n"
        self.__connection.sendall(data)
        response = self.__connection.recv(1024)
        return response

    def __login(self):
        username = base64.b64encode(self.options.get("username").encode("utf-8"))
        password = base64.b64encode(self.options.get("password").encode("utf-8"))
        self.__send(b"AUTH LOGIN")
        self.__send(username)
        response = repr(self.__send(password))
        if int(response[2]) != 2:
            raise RuntimeError("Auth failed")

    def close(self):
        if self.__connection:
            self.__connection.close()
