from core.config import NotificationTypes
from .default_template import default_template

__all__ = (
    'HTML_MAPPER',
)

HTML_MAPPER = {
    NotificationTypes.NEW_REGISTRATION: default_template,
    NotificationTypes.NOTIFICATION: default_template,
    NotificationTypes.WEEKLY: default_template,
}
