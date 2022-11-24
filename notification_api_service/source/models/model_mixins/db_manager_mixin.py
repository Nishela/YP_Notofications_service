from database import DbManager

__all__ = (
    'DbManagerMixin',
)


class DbManagerMixin:
    """Добавляет в модели менеджера для работы с БД PG"""
    class Config:
        db_manager = DbManager
