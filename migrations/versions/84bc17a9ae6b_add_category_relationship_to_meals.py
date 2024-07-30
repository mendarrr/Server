"""Add category relationship to meals

Revision ID: 84bc17a9ae6b
Revises: 
Create Date: 2024-07-30 20:15:55.240862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84bc17a9ae6b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_meal_category_id_category'), 'category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meal', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_meal_category_id_category'), type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###
