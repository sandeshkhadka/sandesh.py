from os import environ

from dotenv import load_dotenv

import sandesh_py as sandesh

load_dotenv()
smtp_username = environ.get("SMTP_USERNAME")
smtp_password = environ.get("SMTP_PASSWORD")
smtp_host = environ.get("SMTP_HOST")
smtp_port = environ.get("SMTP_PORT")
if not (smtp_username and smtp_password and smtp_host and smtp_port):
    print("No username and password found")
    exit(1)

client = sandesh.SMTPClient(
    smtp_host,
    int(smtp_port),
    {"username": smtp_username, "password": smtp_password},
    # {"notls": True},
)

client.connect()
mail = sandesh.Mail(
    {
        "mailTo": "sandeshkhadka217@gmail.com",
        "mailFrom": "mail@khadkasandesh.com.np",
        "subject": "TEST",
        "body": "TEST CONTWENT",
    }
)
# client.sendMail(mail)
print(client.version())
client.close()
