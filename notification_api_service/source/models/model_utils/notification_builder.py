from email.message import EmailMessage

from jinja2 import Environment, BaseLoader

from core.config import get_settings

__all__ = (
    'NotificationBuilder',
)
settings = get_settings()


class NotificationBuilder:

    @classmethod
    async def async_build_email(cls, email_instance, html_template: str = ''):
        message = EmailMessage()
        message["From"] = settings.mail_config.MAIL_FROM
        message["To"] = ",".join(email_instance.recipients)
        message["Subject"] = email_instance.subject
        if html_template:
            template = Environment(loader=BaseLoader(), enable_async=True).from_string(html_template)
            output = await template.render_async(**email_instance.body.dict())
            message.add_alternative(output, subtype='html')
            return message
        message.set_content('\n'.join(email_instance.body.dict().values()))
        return message

    @classmethod
    async def async_build_push(cls, push_instance, template: str = ''):
        return template % (push_instance.user, push_instance.header, push_instance.content)

    @classmethod
    async def async_build_sms(cls, sms_instance, template: str = ''):
        return template % (sms_instance.user, sms_instance.content)
