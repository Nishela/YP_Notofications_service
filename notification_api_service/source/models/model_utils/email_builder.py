from email.message import EmailMessage

from jinja2 import Template

from core.config import get_settings

__all__ = (
    'EmailBuilder',
)
settings = get_settings()


class EmailBuilder:

    @classmethod
    async def async_build(cls, email_instance, html_template):
        message = EmailMessage()
        message["From"] = settings.mail_config.MAIL_USERNAME
        message["To"] = ",".join(email_instance.recipients)
        message["Subject"] = email_instance.subject
        output = await Template(html_template).render_async(**email_instance.body.dict())
        message.add_alternative(output, subtype='html')
        return message
