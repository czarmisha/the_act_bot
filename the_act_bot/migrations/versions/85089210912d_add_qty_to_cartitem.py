"""add qty to cartitem

Revision ID: 85089210912d
Revises: c2521c67d0e1
Create Date: 2024-07-07 23:34:54.797946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85089210912d'
down_revision: Union[str, None] = 'c2521c67d0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'brands', ['name'])
    op.add_column('cart_items', sa.Column('quantity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart_items', 'quantity')
    op.drop_constraint(None, 'brands', type_='unique')
    # ### end Alembic commands ###
