"""empty message

Revision ID: 181d6b03fd86
Revises: 
Create Date: 2025-06-21 12:19:20.708313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '181d6b03fd86'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genre', sa.String(length=40), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('genre')

    # ### end Alembic commands ###
