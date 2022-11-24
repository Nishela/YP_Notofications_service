from database import DbManager

__all__ = (
    'DbManagerMixin',
)


class DbManagerMixin:
    """Добавляет в модели менеджера для работы с БД PG"""
    class ManagerConfig:
        db_manager = DbManager
