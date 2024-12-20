"""empty message

Revision ID: 2c1a032b8bd2
Revises: a52c300c58f9
Create Date: 2024-12-20 16:48:05.885687

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2c1a032b8bd2'
down_revision = 'a52c300c58f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('show', schema=None) as batch_op:
        batch_op.alter_column('start_time',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('show', schema=None) as batch_op:
        batch_op.alter_column('start_time',
               existing_type=sa.String(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)

    # ### end Alembic commands ###
