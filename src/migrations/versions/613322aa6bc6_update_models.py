"""Update models

Revision ID: 613322aa6bc6
Revises: 98aff85f4878
Create Date: 2023-07-01 22:34:56.477311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '613322aa6bc6'
down_revision = '98aff85f4878'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('track_activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_activity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_activity_id'], ['user_activities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('activities')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('duration', sa.INTEGER(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('starting_time', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('track_activities')
    op.drop_table('user_activities')
    # ### end Alembic commands ###
