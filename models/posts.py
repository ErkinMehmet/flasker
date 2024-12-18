from datetime import datetime
from flasker.app import db 


class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255))
    content=db.Column(db.Text)
    #author=db.Column(db.String(255))
    date_posted=db.Column(db.DateTime,default=datetime.now())
    slug=db.Column(db.String(1028))
    # clef étrangère
    poster_id=db.Column(db.Integer,db.ForeignKey('users.id'))