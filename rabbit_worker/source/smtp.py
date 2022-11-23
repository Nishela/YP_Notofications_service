import aiosmtplib
from aiosmtplib import SMTPServerDisconnected, SMTPResponseException, SMTPTimeoutError, SMTP


class SMTPClient:
    def __init__(self, settings):
        self.settings = settings
        self.client = aiosmtplib.SMTP(
            hostname=settings.MAIL_SERVER,
            port=settings.MAIL_PORT,
            use_tls=True,
            validate_certs=False
        )

    async def __aenter__(self) -> SMTP:
        await self.client.connect()
        await self.client.login(self.settings.MAIL_USERNAME, self.settings.MAIL_PASSWORD)

        return self.client

    async def __aexit__(self, exc_type, exc, traceback) -> None:
        if isinstance(exc, (ConnectionError, TimeoutError)):
            self.client.close()
            return

        try:
            await self.client.quit()
        except (SMTPServerDisconnected, SMTPResponseException, SMTPTimeoutError):
            pass
