"""Add appearance and removal dates to ODYCRIM parties

Revision ID: df0221cb4562
Revises: eb90f8b96ee4
Create Date: 2021-03-02 18:39:58.603330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df0221cb4562'
down_revision = 'eb90f8b96ee4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('odycrim_attorneys', sa.Column('appearance_date', sa.Date(), nullable=True))
    op.add_column('odycrim_attorneys', sa.Column('appearance_date_str', sa.String(), nullable=True))
    op.add_column('odycrim_attorneys', sa.Column('removal_date', sa.Date(), nullable=True))
    op.add_column('odycrim_attorneys', sa.Column('removal_date_str', sa.String(), nullable=True))
    op.add_column('odycrim_involved_parties', sa.Column('appearance_date', sa.Date(), nullable=True))
    op.add_column('odycrim_involved_parties', sa.Column('appearance_date_str', sa.String(), nullable=True))
    op.add_column('odycrim_involved_parties', sa.Column('removal_date', sa.Date(), nullable=True))
    op.add_column('odycrim_involved_parties', sa.Column('removal_date_str', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('odycrim_involved_parties', 'removal_date_str')
    op.drop_column('odycrim_involved_parties', 'removal_date')
    op.drop_column('odycrim_involved_parties', 'appearance_date_str')
    op.drop_column('odycrim_involved_parties', 'appearance_date')
    op.drop_column('odycrim_attorneys', 'removal_date_str')
    op.drop_column('odycrim_attorneys', 'removal_date')
    op.drop_column('odycrim_attorneys', 'appearance_date_str')
    op.drop_column('odycrim_attorneys', 'appearance_date')
    # ### end Alembic commands ###
