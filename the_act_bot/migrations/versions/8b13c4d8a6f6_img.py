"""img

Revision ID: 8b13c4d8a6f6
Revises: 07a2674c3356
Create Date: 2024-06-21 09:55:46.909836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b13c4d8a6f6'
down_revision: Union[str, None] = '07a2674c3356'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('tg_file_path', sa.String(length=100), nullable=True))
    op.add_column('images', sa.Column('tg_file_unique_id', sa.String(length=100), nullable=True))
    op.add_column('images', sa.Column('tg_file_id', sa.String(), nullable=True))
    op.drop_column('images', 'url')
    op.drop_column('images', 'file_unique_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('file_unique_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('images', sa.Column('url', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('images', 'tg_file_id')
    op.drop_column('images', 'tg_file_unique_id')
    op.drop_column('images', 'tg_file_path')
    # ### end Alembic commands ###