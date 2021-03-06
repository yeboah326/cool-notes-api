"""empty message

Revision ID: 47f0634904e1
Revises: 9c3317ce4a7a
Create Date: 2022-01-03 12:09:20.787904

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '47f0634904e1'
down_revision = '9c3317ce4a7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cn_account', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('cn_account', sa.Column('date_updated', sa.DateTime(), nullable=True))
    op.drop_column('cn_account', 'created_on')
    op.drop_column('cn_account', 'updated_on')
    op.add_column('cn_note', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('cn_note', sa.Column('date_updated', sa.DateTime(), nullable=True))
    op.drop_column('cn_note', 'created_on')
    op.drop_column('cn_note', 'updated_on')
    op.add_column('cn_tag', sa.Column('date_updated', sa.DateTime(), nullable=True))
    op.alter_column('cn_tag', 'date_created',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cn_tag', 'date_created',
               existing_type=sa.DATE(),
               nullable=False)
    op.drop_column('cn_tag', 'date_updated')
    op.add_column('cn_note', sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('cn_note', sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('cn_note', 'date_updated')
    op.drop_column('cn_note', 'date_created')
    op.add_column('cn_account', sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('cn_account', sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('cn_account', 'date_updated')
    op.drop_column('cn_account', 'date_created')
    # ### end Alembic commands ###
