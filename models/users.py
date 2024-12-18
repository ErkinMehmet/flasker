from datetime import datetime
from flasker.app import db 
from flask_login import LoginManager,login_required,UserMixin,logout_user,current_user,login_user
from werkzeug.security import generate_password_hash,check_password_hash


class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(150),nullable=False,unique=True)
    favorite_color=db.Column(db.String(120))
    createdAt=db.Column(db.DateTime,default=datetime.now())
    #mdp
    password_hash=db.Column(db.String(1028),nullable=False)
    posts=db.relationship('Posts',backref='poster')
    admin = db.Column(db.Boolean, default=False)
    about_author=db.Column(db.Text(500),nullable=True)
    profile_pic=db.Column(db.String(1028),nullable=True)

    @property
    def password(self):
        raise AttributeError("Le mdp n'est pas lisible")
    
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<Name %r>' % self.name