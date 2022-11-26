from database import DbManager, AuthManager

__all__ = (
    'ManagerMixin',
)


class ManagerMixin:
    """Добавляет в модели менеджера для работы с БД PG"""
    class ManagerConfig:
        db_manager = DbManager
        auth_manager = AuthManager
