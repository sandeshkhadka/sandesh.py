import base64
import socket
from typing import TypedDict


class SMTPOptions(TypedDict):
    username: str
    password: str


class Mail(TypedDict):
    mailTo: str
    mailFrom: str
    subject: str
    body: str


class SMTPClient:
    def __init__(self, host: str, port: int, options: SMTPOptions) -> None:
        self.host: str = host
        self.port: int = port
        self.options = options
        self.__loggedIn = False

    def __del__(self):
        self.close()

    def connect(self) -> None:
        self.__connection = socket.create_connection((self.host, self.port))
        response = repr(self.__connection.recv(1024))
        code = response[2:5]
        if code != "220":
            raise RuntimeError(f"Couldn't connect to {self.host} at port {self.port}")
        self.__login()

    def __send(self, data: bytes, noWait=False):
        data = data + b"\r\n"
        self.__connection.sendall(data)
        if noWait:
            return b"noWait"
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
        self.__loggedIn = True

    def sendMail(self, mail: Mail):
        if not self.__connection:
            self.connect()
        if not self.__loggedIn:
            self.__login()

        text = mail.get("body").encode("utf-8")
        mailTo = mail.get("mailTo").encode("utf-8")
        mailFrom = mail.get("mailFrom").encode("utf-8")
        subject = mail.get("subject").encode("utf-8")
        self.__send(b"MAIL FROM: <" + mailFrom + b">")
        self.__send(b"RCPT TO: <" + mailTo + b">")
        self.__send(b"DATA")
        self.__send(b"Subject: " + subject, noWait=True)
        self.__send(b"", noWait=True)
        self.__send(text, noWait=True)
        return repr(self.__send(b"."))

    def close(self):
        if self.__connection:
            self.__connection.close()
