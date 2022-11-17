from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader

from core.config import get_settings

settings = get_settings()


class EmailBuilder:

    @classmethod
    async def async_build(cls, model):
        message = EmailMessage()
        message["From"] = settings.mail_config.MAIL_USERNAME
        message["To"] = ",".join(model.recipients)
        message["Subject"] = model.subject

        template = await cls.__async_get_template()
        output = await template.render_async(**model.body.dict())
        message.add_alternative(output, subtype='html')
        return message

    @classmethod
    async def __async_get_template(cls, template_name='mail.html'):
        return (
            Environment(loader=FileSystemLoader(settings.mail_config.TEMPLATE_FOLDER), enable_async=True)
            .get_template(template_name)
        )
