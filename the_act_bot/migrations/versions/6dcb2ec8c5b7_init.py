"""init

Revision ID: 6dcb2ec8c5b7
Revises: 
Create Date: 2024-06-05 10:29:33.058631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6dcb2ec8c5b7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_brands_created'), 'brands', ['created'], unique=False)
    op.create_table('discounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('FIXED', 'PERCENT', 'PROMO', name='discounttypeenums'), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_discounts_created'), 'discounts', ['created'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('type', sa.Enum('USER', 'ADMIN', 'SYSTEM', name='usertypeenums'), nullable=False),
    sa.Column('lang', sa.Enum('EN', 'RU', 'UZ', name='languageenums'), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_created'), 'users', ['created'], unique=False)
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=False)
    op.create_table('carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_carts_created'), 'carts', ['created'], unique=False)
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'brand_id')
    )
    op.create_index(op.f('ix_categories_created'), 'categories', ['created'], unique=False)
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_created'), 'payments', ['created'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('discount_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['discount_id'], ['discounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_created'), 'products', ['created'], unique=False)
    op.create_table('cart_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cart_items_created'), 'cart_items', ['created'], unique=False)
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_created'), 'images', ['created'], unique=False)
    op.create_table('product_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_id', 'category_id')
    )
    op.create_index(op.f('ix_product_categories_created'), 'product_categories', ['created'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_categories_created'), table_name='product_categories')
    op.drop_table('product_categories')
    op.drop_index(op.f('ix_images_created'), table_name='images')
    op.drop_table('images')
    op.drop_index(op.f('ix_cart_items_created'), table_name='cart_items')
    op.drop_table('cart_items')
    op.drop_index(op.f('ix_products_created'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_payments_created'), table_name='payments')
    op.drop_table('payments')
    op.drop_index(op.f('ix_categories_created'), table_name='categories')
    op.drop_table('categories')
    op.drop_index(op.f('ix_carts_created'), table_name='carts')
    op.drop_table('carts')
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.drop_index(op.f('ix_users_created'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_discounts_created'), table_name='discounts')
    op.drop_table('discounts')
    op.drop_index(op.f('ix_brands_created'), table_name='brands')
    op.drop_table('brands')
    # ### end Alembic commands ###
