import base64
import socket
import ssl

from .mailer import createDataQueue
from .types import Mail, SMTPAuth, SMTPOptions


class SMTPClient:
    def __init__(
        self, host: str, port: int, auth: SMTPAuth, options: SMTPOptions | None = None
    ) -> None:
        self.hostname: str = host
        self.port: int = port
        self.auth = auth
        self.options = options
        self.__loggedIn = False
        self.__starttls = False

    def __del__(self):
        self.close()

    def connect(self) -> None:
        self.__connection = socket.create_connection((self.hostname, self.port))

        response = repr(self.__connection.recv(1024))
        code = response[2:5]
        if code != "220":
            raise RuntimeError(
                f"Couldn't connect to {self.hostname} at port {self.port}"
            )

        self.__handshake()

        if self.options and self.options.get("notls"):
            self.__login()
            return
        if not self.__starttls:
            raise RuntimeError(
                """Server doesn't support TLS connection. Explicitly set \"notls\"=True in options."""
            )

        self.__connection = self.__upgradeToTls()
        self.__login()

    def __handshake(self):
        response = repr(self.__send(b"EHLO " + self.hostname.encode("utf-8")))
        if "starttls" in response.lower():
            self.__starttls = True

    def __send(self, data: bytes, noWait=False):
        data = data + b"\r\n"
        self.__connection.sendall(data)
        if noWait:
            return b"noWait"
        response = self.__connection.recv(1024)
        return response

    def __login(self):
        username = base64.b64encode(self.auth.get("username").encode("utf-8"))
        password = base64.b64encode(self.auth.get("password").encode("utf-8"))
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

        dataQueue = createDataQueue(mail)
        for data in dataQueue:
            self.__send(data.get("data"), noWait=data.get("noWait"))

        return repr(self.__send(b"."))

    def version(self):
        if isinstance(self.__connection, ssl.SSLSocket):
            return self.__connection.version()
        else:
            return "No tls"

    def __upgradeToTls(self):
        context = ssl.create_default_context()
        if not self.options:
            context.options |= ssl.OP_NO_TLSv1
            context.options |= ssl.OP_NO_TLSv1_1
            context.verify_mode = ssl.CERT_REQUIRED

        if self.options:
            if not self.options.get("tlsOlder"):
                context.options |= ssl.OP_NO_TLSv1
                context.options |= ssl.OP_NO_TLSv1_1

            if not self.options.get("disableHostValidation"):
                context.verify_mode = ssl.CERT_REQUIRED

        self.__send(b"STARTTLS")
        return context.wrap_socket(self.__connection, server_hostname=self.hostname)

    def close(self):
        if self.__connection:
            self.__connection.close()
