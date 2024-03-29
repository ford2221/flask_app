"""modification tables

Revision ID: 459b33ebdab8
Revises: d7acef3338df
Create Date: 2021-02-22 13:55:52.286623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '459b33ebdab8'
down_revision = 'd7acef3338df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sells',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('surname', sa.String(length=255), nullable=True),
    sa.Column('company', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sell_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sell_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['sell_id'], ['sells.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sell_products')
    op.drop_table('sells')
    # ### end Alembic commands ###
