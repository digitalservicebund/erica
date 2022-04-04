"""create new request type grundsteuer

Revision ID: d57d4d27a115
Revises: 5313b3c6d8ec
Create Date: 2022-04-04 09:09:25.063826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd57d4d27a115'
down_revision = '5313b3c6d8ec'
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE requesttype ADD VALUE 'grundsteuer'")


def downgrade():
    with op.get_context().autocommit_block():
        op.execute("DROP TYPE IF EXISTS requesttype")
        op.execute("CREATE TYPE requesttype AS ENUM('freischalt_code_request', 'freischalt_code_activate', 'freischalt_code_revocate', 'check_tax_number', 'send_est')")
