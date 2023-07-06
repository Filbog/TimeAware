"""some changes to the track_activities table

Revision ID: 154cd6a3b0ef
Revises: 613322aa6bc6
Create Date: 2023-07-06 00:26:55.412290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '154cd6a3b0ef'
down_revision = '613322aa6bc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('track_activities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_time', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('end_time', sa.DateTime(timezone=True), nullable=True))
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('track_activities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DATETIME(), nullable=True))
        batch_op.drop_column('end_time')
        batch_op.drop_column('start_time')

    # ### end Alembic commands ###
