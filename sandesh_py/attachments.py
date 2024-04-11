import base64
import os
from mimetypes import MimeTypes


def attach(attachments, queue, boundary):
    mime = MimeTypes()
    for attachment_path in attachments:
        if os.path.exists(attachment_path):
            file_size_in_kb = os.path.getsize(attachment_path) / 1024
            file_size_limit_kb = 20 * 1024  # 20MB
            if file_size_in_kb > file_size_limit_kb:
                raise Exception(
                    "File size limit exceeded by attachment: " + attachment_path
                )
            with open(attachment_path, "rb") as attachment_file:
                (mimetype, _) = mime.guess_type(attachment_path)
                if mimetype:
                    filetype = mimetype.split("/")[1]
                else:
                    mimetype = "application/octet-stream"
                    filetype = "binary"
                attachment_data = attachment_file.read()
                filename = os.path.basename(attachment_path).encode("utf-8")
                queue.append({"data": b"--" + boundary, "noWait": True})
                queue.append(
                    {
                        "data": b"Content-Type: " + mimetype.encode("utf-8"),
                        "noWait": True,
                    }
                )
                queue.append(
                    {
                        "data": b'Content-Disposition: attachment; filename="'
                        + filename
                        + b'"',
                        "noWait": True,
                    }
                )
                attachment_data_base64 = base64.b64encode(attachment_data)
                queue.append(
                    {
                        "data": b"Content-Transfer-Encoding: base64",
                        "noWait": True,
                    }
                )
                queue.append({"data": attachment_data_base64, "noWait": True})

                queue.append(
                    {
                        "data": b"<base64-encoded-"
                        + filetype.encode("utf-8")
                        + b"-data>",
                        "noWait": True,
                    }
                )
