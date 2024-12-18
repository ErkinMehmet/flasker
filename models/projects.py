from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flasker.app import db 

class Projects(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    skills = db.Column(db.String(500), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    is_public = db.Column(db.Boolean, default=True)
    featured_image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, nullable=True)  # Foreign key for the user who created the project
    updated_by = db.Column(db.Integer, nullable=True)  # Foreign key for the user who updated the project

    def __repr__(self):
        return f"<Project {self.title}>"
