"""add projects3

Revision ID: 74351bc6bcca
Revises: 6301a1983f64
Create Date: 2024-12-18 00:40:07.975959

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '74351bc6bcca'
down_revision = '6301a1983f64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Articles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('subtitle', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('views_count', sa.Integer(), nullable=False),
    sa.Column('shares_count', sa.Integer(), nullable=False),
    sa.Column('newsletter_priority', sa.Integer(), nullable=False),
    sa.Column('published_date', sa.DateTime(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=False),
    sa.Column('featured', sa.Boolean(), nullable=False),
    sa.Column('published', sa.Boolean(), nullable=False),
    sa.Column('newsletter', sa.Boolean(), nullable=False),
    sa.Column('soquij', sa.Boolean(), nullable=False),
    sa.Column('tags', sa.Text(), nullable=True),
    sa.Column('article_category', sa.Integer(), nullable=False),
    sa.Column('external_url', sa.Text(), nullable=True),
    sa.Column('theme_id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('featured_image_id', sa.Integer(), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('articles')
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subtitle', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('skills', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('skills')
        batch_op.drop_column('subtitle')

    op.create_table('articles',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('subtitle', mysql.TEXT(), nullable=True),
    sa.Column('summary', mysql.TEXT(), nullable=True),
    sa.Column('content', mysql.TEXT(), nullable=True),
    sa.Column('views_count', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('shares_count', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('newsletter_priority', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('published_date', mysql.DATETIME(), nullable=True),
    sa.Column('start_date', mysql.DATETIME(), nullable=True),
    sa.Column('end_date', mysql.DATETIME(), nullable=True),
    sa.Column('public', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('featured', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('published', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('newsletter', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('soquij', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('tags', mysql.TEXT(), nullable=True),
    sa.Column('article_category', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('external_url', mysql.TEXT(), nullable=True),
    sa.Column('theme_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('organization_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('author_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('featured_image_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('region_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=False),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('updated_by', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('Articles')
    # ### end Alembic commands ###