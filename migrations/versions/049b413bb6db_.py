"""empty message

Revision ID: 049b413bb6db
Revises: 
Create Date: 2020-04-29 01:25:43.337069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '049b413bb6db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('actors')
    op.drop_table('movie')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('boxoffice', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='movie_pkey')
    )
    op.create_table('actors',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('firstname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('lastname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='actors_pkey')
    )
    # ### end Alembic commands ###
