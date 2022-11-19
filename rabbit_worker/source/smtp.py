import aiosmtplib


async def init_smtp(settings):
    email_client = aiosmtplib.SMTP(
        hostname=settings.MAIL_SERVER,
        port=settings.MAIL_PORT,
        use_tls=True,
        validate_certs=False
    )
    await email_client.connect()
    await email_client.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
    return email_client
