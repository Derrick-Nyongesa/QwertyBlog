"""added bio and profile picture column

Revision ID: 904d72c76f4a
Revises: 4ad6d590a93f
Create Date: 2021-04-29 15:14:22.649619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '904d72c76f4a'
down_revision = '4ad6d590a93f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bio', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('profile_pic_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic_path')
    op.drop_column('users', 'bio')
    # ### end Alembic commands ###
