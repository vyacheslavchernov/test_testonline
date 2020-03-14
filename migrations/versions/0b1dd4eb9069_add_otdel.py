"""add otdel

Revision ID: 0b1dd4eb9069
Revises: d05441283eb8
Create Date: 2020-03-13 22:54:50.067831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b1dd4eb9069'
down_revision = 'd05441283eb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questions')
    op.drop_table('answers')
    op.add_column('user', sa.Column('otdel', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_otdel'), 'user', ['otdel'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_otdel'), table_name='user')
    op.drop_column('user', 'otdel')
    op.create_table('answers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('question_id', sa.INTEGER(), nullable=True),
    sa.Column('answer', sa.VARCHAR(length=64), nullable=True),
    sa.Column('yes_no', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('question', sa.VARCHAR(length=500), nullable=True),
    sa.Column('q_type', sa.VARCHAR(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('question')
    )
    # ### end Alembic commands ###