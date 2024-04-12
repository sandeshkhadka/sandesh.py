# Sandesh - Send Mail 🕊️

Basic implementaion of SMTP client using TCP communication with the SMTP server using the `socket` module.

## Installation

```shell
pip install sandesh.py
```

## Usage

```python
from sandesh_py import smtp

auth: smtp.SMTPAuth = {
    "username": YOUR_SMTP_USERNAME,
    "password": YOUR_SMTP_PASSWORD,
}
options: smtp.SMTPOptions = {"notls": False}
client = smtp.SMTPClient(SMTP_SERVER_HOST, SMTP_PORT, auth, options)

client.connect()
mail = smtp.Mail(
    {
        "mailTo": "receiver@email.com",
        "mailFrom": "sender@email.com",
        "subject": "Mail subject",
        "body": "This is demonstartaion of use of sandesh_py package",
        "attachment": [
            "/path/to/attachment/1",
            "/path/to/attachment/2",
        ],
    }
)
print(client.sendMail(mail))
client.close()

```

## ToDo List

- [x] Support authentication using username and password
- [x] Implement SSL/TLS encryption for secure communication
- [x] Add support for MIME to handle attachments and alternative content types
- [ ] Support Oath and API authentication
- [ ] Connection Pooling and Asynchronous Delivery
