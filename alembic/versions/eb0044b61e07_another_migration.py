"""Another Migration

Revision ID: eb0044b61e07
Revises: f848625a4976
Create Date: 2026-03-09 23:08:19.543403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb0044b61e07'
down_revision: Union[str, Sequence[str], None] = 'f848625a4976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('book') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.alter_column('average_rating',
               existing_type=sa.VARCHAR(),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.alter_column('rating_count',
               existing_type=sa.FLOAT(),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.create_foreign_key('fk_book_user', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    with op.batch_alter_table('book') as batch_op:
        batch_op.drop_constraint('fk_book_user', type_='foreignkey')
        batch_op.alter_column('rating_count',
               existing_type=sa.Integer(),
               type_=sa.FLOAT(),
               existing_nullable=True)
        batch_op.alter_column('average_rating',
               existing_type=sa.Float(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.drop_column('user_id')