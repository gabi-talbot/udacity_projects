"""empty message

Revision ID: fcbfc4b976fd
Revises: 324ef3539a7e
Create Date: 2024-12-19 12:16:27.861540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcbfc4b976fd'
down_revision = '324ef3539a7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_talent', sa.Boolean(), nullable=True))
        batch_op.drop_column('seeking_venue')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.drop_column('seeking_talent')

    # ### end Alembic commands ###
