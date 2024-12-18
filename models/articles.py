from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flasker.app import db 

class Articles(db.Model):
    __tablename__ = 'Articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.Text, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    views_count = db.Column(db.Integer, nullable=False, default=0)
    shares_count = db.Column(db.Integer, nullable=False, default=0)
    newsletter_priority = db.Column(db.Integer, nullable=False, default=0)
    published_date = db.Column(db.DateTime, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    public = db.Column(db.Boolean, nullable=False, default=False)
    featured = db.Column(db.Boolean, nullable=False, default=False)
    published = db.Column(db.Boolean, nullable=False, default=False)
    newsletter = db.Column(db.Boolean, nullable=False, default=False)
    soquij = db.Column(db.Boolean, nullable=False, default=False)
    tags = db.Column(db.Text, nullable=True)
    article_category = db.Column(db.Integer, nullable=False, default=0)
    external_url = db.Column(db.Text, nullable=True)
    theme_id = db.Column(db.Integer, nullable=False)
    organization_id = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, nullable=True)
    featured_image_id = db.Column(db.Integer, nullable=True)
    region_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Articles(ID={self.ID}, Title='{self.Title}', Published={self.Published})>"
