"""Initial tables

Revision ID: 4ca660162948
Revises: 
Create Date: 2021-05-04 17:34:35.939864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ca660162948'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('announcements',
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', dlc_oracle_bot.models.guid.GUID(), nullable=False),
    sa.Column('price_id', dlc_oracle_bot.models.guid.GUID(), nullable=True),
    sa.Column('announcement', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assets',
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', dlc_oracle_bot.models.guid.GUID(), nullable=False),
    sa.Column('source_id', dlc_oracle_bot.models.guid.GUID(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('unit_of_account', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prices',
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', dlc_oracle_bot.models.guid.GUID(), nullable=False),
    sa.Column('asset_id', dlc_oracle_bot.models.guid.GUID(), nullable=True),
    sa.Column('period', sa.Text(), nullable=True),
    sa.Column('close_timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.Column('rate', sa.Numeric(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sources',
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', dlc_oracle_bot.models.guid.GUID(), nullable=False),
    sa.Column('label', sa.Text(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sources')
    op.drop_table('prices')
    op.drop_table('assets')
    op.drop_table('announcements')
    # ### end Alembic commands ###
