"""initial 3

Revision ID: 3d00c9b54835
Revises: d981cb0bbcc4
Create Date: 2024-04-07 00:50:06.650112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d00c9b54835'
down_revision: Union[str, None] = 'd981cb0bbcc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('film', sa.Column('id_type', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_film_type_id', 'film', 'type', ['id_type'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_film_type_id', 'film', type_='foreignkey')
    op.drop_column('film', 'id_type')
    op.drop_table('type')
    # ### end Alembic commands ###