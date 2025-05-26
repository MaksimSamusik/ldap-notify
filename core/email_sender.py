import os
import ssl
import logging
from email.mime.text import MIMEText
import aiosmtplib
from dotenv import load_dotenv
from core.settings import mail_settings

load_dotenv()

logger = logging.getLogger(__name__)


class EmailSender:
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")

    def __init__(self, email: str, name: str):
        if not email or not name:
            raise ValueError("Email and name cannot be empty")
        self.email = email
        self.name = name

    def create_smtp_client(self) -> aiosmtplib.SMTP:
        ssl_context = ssl.create_default_context()
        return aiosmtplib.SMTP(
            hostname=self.SMTP_SERVER,
            port=self.SMTP_PORT,
            use_tls=True,
            tls_context=ssl_context,
            timeout=10
        )

    def create_message(self, body: str = None, subject: str = None) -> MIMEText:
        body = body or mail_settings.body
        subject = subject or mail_settings.subject

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.SMTP_USER
        msg['To'] = self.email
        return msg

    async def send_email(self, smtp_client=None, msg=None) -> bool:
        try:
            smtp_client = smtp_client or self.create_smtp_client()
            msg = msg or self.create_message()

            await smtp_client.connect()
            if not smtp_client.is_connected:
                logger.error(f"Failed to connect to SMTP server")
                return False

            await smtp_client.login(self.SMTP_USER, self.SMTP_PASS)
            await smtp_client.send_message(msg)
            logger.info(f"Email successfully sent to {self.email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email to {self.email}: {str(e)}", exc_info=True)
            return False

        finally:
            if smtp_client and smtp_client.is_connected:
                await smtp_client.quit()
