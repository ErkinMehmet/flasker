from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

class UserForm(FlaskForm):
        name=StringField("Nom",validators=[DataRequired()])
        username=StringField("Nom d'utilisateur",validators=[DataRequired()])
        email=StringField("Email",validators=[DataRequired()])
        favorite_color=StringField("Couleur favorite")
        about_author=StringField("Description",widget=TextArea())
        password_hash=PasswordField('Mot de passe',validators=[DataRequired(),EqualTo('password_hash2',message="Les deux mdps devraient être pareils")])
        password_hash2=PasswordField('Confirmer le mot de passe',validators=[DataRequired()])
        admin=BooleanField('Admin', default=False)
        profile_pic=FileField("Photo profil")
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
    content=CKEditorField('Content',validators=[DataRequired()])#StringField("Contenu",validators=[DataRequired()],widget=TextArea())
    slug=StringField("Slug",validators=[DataRequired()])
    submit=SubmitField("Soumettre")

class LoginForm(FlaskForm):
    username=StringField("Nom d'utilisateur",validators=[DataRequired()])
    password=PasswordField('Mot de passe',validators=[DataRequired()])
    submit=SubmitField("Soumettre")

class SearchForm(FlaskForm):
     searched=StringField("Chercher",validators=[DataRequired()])
     submit=SubmitField("Soumettre")
