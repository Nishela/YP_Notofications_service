from fastapi_mail import MessageSchema, MessageType

__all__ = (
    'EmailBuilder',
)


class EmailBuilder:

    @classmethod
    async def async_build_by_template(cls, email_instance):
        return MessageSchema(
            subject=email_instance.subject,
            recipients=email_instance.recipients,
            template_body=email_instance.body,
            subtype=MessageType.html,
        )
