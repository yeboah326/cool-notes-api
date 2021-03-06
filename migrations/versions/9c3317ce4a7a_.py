"""empty message

Revision ID: 9c3317ce4a7a
Revises: 23a1b3bfe870
Create Date: 2022-01-03 10:33:05.844968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c3317ce4a7a'
down_revision = '23a1b3bfe870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cn_account', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.add_column('cn_account', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.drop_column('cn_account', 'date_created')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cn_account', sa.Column('date_created', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_column('cn_account', 'updated_on')
    op.drop_column('cn_account', 'created_on')
    # ### end Alembic commands ###
