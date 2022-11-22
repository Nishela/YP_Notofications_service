from email.message import EmailMessage

from jinja2 import Environment, BaseLoader

from core.config import get_settings

__all__ = (
    'EmailBuilder',
)
settings = get_settings()


class EmailBuilder:

    @classmethod
    async def async_build(cls, email_instance, html_template: str = ''):
        message = EmailMessage()
        message["From"] = settings.mail_config.MAIL_FROM
        message["To"] = ",".join(email_instance.recipients)
        message["Subject"] = email_instance.subject
        template = Environment(loader=BaseLoader(), enable_async=True).from_string(html_template)
        output = await template.render_async(**email_instance.body.dict())
        message.add_alternative(output, subtype='html')
        return message
