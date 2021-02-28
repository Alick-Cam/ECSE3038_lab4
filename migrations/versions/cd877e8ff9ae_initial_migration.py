"""Initial Migration

Revision ID: cd877e8ff9ae
Revises: 
Create Date: 2021-02-27 23:47:56.061726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd877e8ff9ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Tank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('lat', sa.String(), nullable=True),
    sa.Column('long', sa.String(), nullable=True),
    sa.Column('percentage_full', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Tank')
    # ### end Alembic commands ###