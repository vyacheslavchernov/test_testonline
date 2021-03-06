"""Init migration.

Revision ID: b47d7e19b467
Revises: 
Create Date: 2020-03-15 19:36:43.990326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b47d7e19b467'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=500), nullable=True),
    sa.Column('q_type', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('question')
    )
    op.create_table('test_answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('question', sa.String(length=500), nullable=True),
    sa.Column('answer', sa.String(length=500), nullable=True),
    sa.Column('user_answer', sa.String(length=500), nullable=True),
    sa.Column('result', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('otdel', sa.String(length=64), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_date'), 'user', ['date'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('answer', sa.String(length=500), nullable=True),
    sa.Column('yes_no', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_date'), table_name='user')
    op.drop_table('user')
    op.drop_table('test_answers')
    op.drop_table('questions')
    # ### end Alembic commands ###
