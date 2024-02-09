from os import environ

from dotenv import load_dotenv

from sandesh import smtp

load_dotenv()
smtp_username = environ.get("SMTP_USERNAME")
smtp_password = environ.get("SMTP_PASSWORD")
smtp_host = environ.get("SMTP_HOST")
smtp_port = environ.get("SMTP_PORT")
if not (smtp_username and smtp_password and smtp_host and smtp_port):
    print("No username and password found")
    exit(1)

client = smtp.SMTPClient(
    smtp_host,
    int(smtp_port),
    {"username": smtp_username, "password": smtp_password},
)

client.connect()

client.close()
