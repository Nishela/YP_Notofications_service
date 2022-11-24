from core.config import NotificationTypes
from .default_template import default_template

__all__ = (
    'HTML_MAPPER',
)

HTML_MAPPER = {
    NotificationTypes.EMAIL: default_template,
    NotificationTypes.PUSH: default_template,
    NotificationTypes.SMS: default_template,
}
