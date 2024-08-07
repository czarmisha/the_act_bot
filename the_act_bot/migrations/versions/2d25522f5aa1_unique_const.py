"""unique const

Revision ID: 2d25522f5aa1
Revises: 85089210912d
Create Date: 2024-07-08 19:51:36.631833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d25522f5aa1'
down_revision: Union[str, None] = '85089210912d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'cart_items', ['cart_id', 'product_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart_items', type_='unique')
    # ### end Alembic commands ###
