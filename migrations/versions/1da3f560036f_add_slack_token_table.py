"""Add slack_token table"""

from alembic import op
import sqlalchemy as sa


revision = '1da3f560036f'
down_revision = None


def upgrade():
    op.create_table('slack_token',
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('room', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )


def downgrade():
    op.drop_table('slack_token')
