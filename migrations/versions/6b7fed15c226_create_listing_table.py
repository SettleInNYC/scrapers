"""Create listing table

Revision ID: 6b7fed15c226
Revises: 
Create Date: 2017-10-12 16:34:57.968731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b7fed15c226'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'listing',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('zipcode', sa.String(5)),
        sa.Column('text', sa.Unicode()),
        sa.Column('price', sa.Float),
        sa.Column('scraped_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('listing')
