"""empty message

Revision ID: 0ac44ba6a7c3
Revises: 628fc182f32e
Create Date: 2021-02-14 12:09:31.380072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ac44ba6a7c3'
down_revision = '628fc182f32e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('email_confirmed_at', sa.DateTime(), nullable=True))
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'email_confirmed_at')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
