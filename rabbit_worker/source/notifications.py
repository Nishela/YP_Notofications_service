class NotificationSender:
    @staticmethod
    def send_notification(client, notification_type: str, message: bytes):
        func = getattr(NotificationSender, f'__send_{notification_type}')
        func(message)

    def __send_new_registration(self):
        pass

    def __send_notification(self):
        pass

    def __send_weekly(self):
        pass
