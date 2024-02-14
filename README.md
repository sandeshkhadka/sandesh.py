# Sandesh - Send Mail 🕊️

Basic implementaion of SMTP client using TCP communication with the SMTP server using the `socket` module.

## Usage

```python

import sandesh_py as sandesh
auth = {"username": SMTP_USERNAME, "password": SMTP_PASSWORD},
options = {"notls": False}
client = sandesh.SMTPClient(
    SMTP_HOST,
    SMTP_PORT,
    auth,
    options
t

client.connect()
mail = smtp.Mail(
    {
        "mailTo": "recipient@example.com",
        "mailFrom": "sender@example.com",
        "subject": "Email Subject",
        "body": "Email Body",
    }
)
client.sendMail(mail)
client.close()


```

## ToDo List

- [x] Support authentication using username and password
- [ ] Implement SSL/TLS encryption for secure communication
- [ ] Add support for MIME to handle attachments and alternative content types
- [ ] Support additional authentication mechanisms such as OAuth or API keys
- [ ] Connection Pooling and Asynchronous Delivery
