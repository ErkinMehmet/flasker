from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea

class UserForm(FlaskForm):
        name=StringField("Nom",validators=[DataRequired()])
        username=StringField("Nom d'utilisateur",validators=[DataRequired()])
        email=StringField("Email",validators=[DataRequired()])
        favorite_color=StringField("Couleur favorite")
        password_hash=PasswordField('Mot de passe',validators=[DataRequired(),EqualTo('password_hash2',message="Les deux mdps devraient être pareils")])
        password_hash2=PasswordField('Confirmer le mot de passe',validators=[DataRequired()])
        submit=SubmitField("Soumettre")

class PwdForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    password_hash=PasswordField('Mot de passe',validators=[DataRequired()])
    submit=SubmitField("Soumettre")

class NamerForm(FlaskForm):
    name=StringField("Quel est votre nom",validators=[DataRequired()])
    submit=SubmitField("Soumettre")
    
class PostForm(FlaskForm):
    title=StringField("Titre",validators=[DataRequired()])
    content=StringField("Contenu",validators=[DataRequired()],widget=TextArea())
    author=StringField("Autheur",validators=[DataRequired()])
    slug=StringField("Slug",validators=[DataRequired()])
    submit=SubmitField("Soumettre")

class LoginForm(FlaskForm):
    username=StringField("Nom d'utilisateur",validators=[DataRequired()])
    password=PasswordField('Mot de passe',validators=[DataRequired()])
    submit=SubmitField("Soumettre")