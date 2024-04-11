from datetime import datetime

from .attachments import attach
from .types import DataNode, Mail


def createDataQueue(mail: Mail) -> list[DataNode]:
    queue: list[DataNode] = []

    mailFrom = mail.get("mailFrom").encode("utf-8")
    mailTo = mail.get("mailTo").encode("utf-8")
    subject = mail.get("subject").encode("utf-8")
    text = mail.get("body").encode("utf-8")

    boundary = f'BOUNDARY_{"".join(datetime.now().ctime().split(" "))}'.encode("utf-8")

    queue.append({"data": b"MAIL FROM: <" + mailFrom + b">", "noWait": False})
    queue.append({"data": b"RCPT TO: <" + mailTo + b">", "noWait": False})

    # Email Headers
    queue.append({"data": b"DATA", "noWait": False})
    queue.append({"data": b"From: " + mailFrom, "noWait": True})
    queue.append({"data": b"To: " + mailTo, "noWait": True})
    queue.append({"data": b"Subject: " + subject, "noWait": True})
    queue.append({"data": b"MIME-Version: 1.0", "noWait": True})
    queue.append(
        {
            "data": b"Content-Type: multipart/mixed; boundary=" + boundary,
            "noWait": True,
        }
    )
    queue.append({"data": b"", "noWait": True})
    queue.append({"data": b"--" + boundary, "noWait": True})
    queue.append({"data": b"Content-Type: text/plain", "noWait": True})
    queue.append({"data": b"", "noWait": True})
    queue.append({"data": text, "noWait": True})
    queue.append({"data": b"", "noWait": True})

    attachments = mail.get("attachment")

    if attachments:
        attach(attachments, queue, boundary)

    queue.append({"data": b"--" + boundary + b"--", "noWait": True})
    queue.append({"data": b"", "noWait": True})
    return queue
