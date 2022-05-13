"""Added Erica_Request_Table

Revision ID: 5313b3c6d8ec
Revises: 
Create Date: 2022-03-24 20:59:12.346075

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5313b3c6d8ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():    
    op.execute('DROP TABLE IF EXISTS erica_request')
    op.execute('DROP TYPE IF EXISTS requesttype')
    op.execute('DROP TYPE IF EXISTS status')
    op.create_table('erica_request',
                    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('creator_id', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type',
                              sa.Enum('freischalt_code_request', 'freischalt_code_activate', 'freischalt_code_revocate',
                                      'check_tax_number', 'send_est', name='requesttype'), nullable=True),
                    sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('result', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('status', sa.Enum('new', 'scheduled', 'processing', 'failed', 'success', name='status'),
                              nullable=True),
                    sa.Column('error_code', sa.String(), nullable=True),
                    sa.Column('error_message', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('erica_request')
    op.execute('DROP TYPE IF EXISTS requesttype')
    op.execute('DROP TYPE IF EXISTS status')
