"""Rename room column to channel"""

from alembic import op
import sqlalchemy as sa


revision = 'cd50369c7e22'
down_revision = '1da3f560036f'


def upgrade():
    op.alter_column('slack_token', 'room', new_column_name='channel')


def downgrade():
    op.alter_column('slack_token', 'channel', new_column_name='room')
