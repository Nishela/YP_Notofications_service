"""Init tables

Revision ID: 39ac0b472e32
Revises:
Create Date: 2022-11-21 12:24:57.544670

"""
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
# revision identifiers, used by Alembic.
from sqlalchemy.dialects.postgresql import insert

from core.config import get_settings
from database.tables import Notifications, Templates
from default_templates import HTML_MAPPER

revision = '39ac0b472e32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('name', sa.String(length=256), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('templates',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('body', sa.Text(), nullable=False),
                    sa.Column('notification_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.ForeignKeyConstraint(('notification_id',), ['notifications.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )

    settings = get_settings()
    for notification_type in settings.notification_types:
        notification_data = (uuid4(), notification_type.value)

        op.execute(
            insert(Notifications)
            .values(notification_data)
            .on_conflict_do_nothing()
        )

        op.execute(
            insert(Templates).
            values((uuid4(), HTML_MAPPER.get(notification_type), notification_data[0]))
            .on_conflict_do_nothing()
        )


# ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('templates')
    op.drop_table('notifications')
    # ### end Alembic commands ###
