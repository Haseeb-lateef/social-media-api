"""create post tabele

Revision ID: 43ec4925c94b
Revises: 
Create Date: 2026-07-14 23:05:27.811872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43ec4925c94b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column("title", sa.String(), nullable=False))
    pass
    



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column
