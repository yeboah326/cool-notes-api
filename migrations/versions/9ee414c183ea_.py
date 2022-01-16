"""empty message

Revision ID: 9ee414c183ea
Revises: 47f0634904e1
Create Date: 2022-01-15 08:53:48.562725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ee414c183ea'
down_revision = '47f0634904e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'cn_tag', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cn_tag', type_='unique')
    # ### end Alembic commands ###