"""Adicionando índices

Revision ID: 07616ee666ff
Revises: 2f35508d7011
Create Date: 2024-12-08 20:17:45.088876
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "07616ee666ff"
down_revision = "2f35508d7011"
branch_labels = None
depends_on = None


def upgrade():
    # Adicionando índices
    op.create_index("ix_users_name", "Users", ["name"])
    op.create_index("ix_users_time_created", "Users", ["time_created"])
    op.create_index("ix_users_email", "Users", ["email"])
    op.create_index("ix_users_cpf", "Users", ["cpf"])


def downgrade():
    # Removendo os índices criados
    op.drop_index("ix_users_name", table_name="Users")
    op.drop_index("ix_users_time_created", table_name="Users")
    op.drop_index("ix_users_email", table_name="Users")
    op.drop_index("ix_users_cpf", table_name="Users")
