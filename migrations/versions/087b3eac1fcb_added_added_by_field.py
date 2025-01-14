"""added added_by field

Revision ID: 087b3eac1fcb
Revises: 
Create Date: 2023-10-12 23:04:44.077919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '087b3eac1fcb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('opinion', sa.Column('added_by', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('opinion', 'added_by')
    # ### end Alembic commands ###
