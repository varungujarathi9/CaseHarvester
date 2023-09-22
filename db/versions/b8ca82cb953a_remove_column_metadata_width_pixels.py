"""Remove column_metadata.width_pixels

Revision ID: b8ca82cb953a
Revises: d00d41f1ae1f
Create Date: 2021-10-13 17:29:47.246297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8ca82cb953a'
down_revision = 'd00d41f1ae1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('column_metadata', 'width_pixels')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('column_metadata', sa.Column('width_pixels', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###