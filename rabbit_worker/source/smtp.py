import logging

import aiosmtplib


async def init_smtp(settings):
    logging.debug('initializing smtp')
    email_client = aiosmtplib.SMTP(
        hostname=settings.MAIL_SERVER,
        port=settings.MAIL_PORT,
        use_tls=True,
        validate_certs=False
    )
    await email_client.connect()
    await email_client.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
    logging.debug('smtp initialized')
    return email_client
