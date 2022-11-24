from core.config import NotificationTypes
from .default_email_template import email_template_default
from .default_push_template import push_template_default
from .default_sms_template import sms_template_default

__all__ = (
    'HTML_MAPPER',
)

HTML_MAPPER = {
    NotificationTypes.EMAIL: email_template_default,
    NotificationTypes.PUSH: push_template_default,
    NotificationTypes.SMS: sms_template_default,
}
