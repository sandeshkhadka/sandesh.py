from typing import NotRequired, TypedDict


class DataNode(TypedDict):
    data: bytes
    noWait: bool


class SMTPOptions(TypedDict):
    tlsOlder: NotRequired[bool]
    notls: NotRequired[bool]
    disableHostValidation: NotRequired[bool]


class SMTPAuth(TypedDict):
    username: str
    password: str


class Mail(TypedDict):
    mailTo: str
    mailFrom: str
    subject: str
    body: str
    attachment: NotRequired[list[str]]
