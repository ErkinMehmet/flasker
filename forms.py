from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError,SelectField,IntegerField
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

class ClusteringForm(FlaskForm):
    modele = SelectField('Algorithme de Clustering', choices=[('K-Means', 'K-Means'),
                                                             ('DBSCAN', 'DBSCAN'),
                                                             ('Hierarchical', 'Clustering Hiérarchique'),
                                                             ('Gaussian Mixture', 'Mélange Gaussien')],
                         validators=[DataRequired()])
    mesure = SelectField('Mesure', choices=[('Silhouette', 'Silhouette'),
                                            ('Inertie', 'Inertie'),
                                            ('Dunn Index', 'Indice de Dunn')],
                         validators=[DataRequired()])
    colonnes_categories = StringField('Colonnes de catégories', validators=[DataRequired()])
    colonnes_numeriques = StringField('Colonnes numériques', validators=[DataRequired()])
    sql_query = StringField('SQL Query',widget=TextArea(), validators=[DataRequired()])
    random_state = IntegerField('Random State', validators=[DataRequired()], default=42)  # Default value for example
    number_of_clusters = IntegerField('Nombre de Clusters', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

class RegressionForm(FlaskForm):
    modele = SelectField('Algorithme de Régression', choices=[('Régression Linéaire', 'Régression Linéaire'),
                                                              ('Régression Logistique', 'Régression Logistique'),
                                                              ('Arbre de Décision', 'Arbre de Décision'),
                                                              ('Forêt Aléatoire', 'Forêt Aléatoire'),
                                                              ('Support Vector Machine', 'Machine à Vecteurs de Support'),
                                                              ('Ridge', 'Ridge'),
                                                              ('Lasso', 'Lasso')],
                         validators=[DataRequired()])
    mesure = SelectField('Mesure', choices=[('R2', 'R2'),
                                            ('MSE', 'MSE'),
                                            ('Exactitude', 'Exactitude')],
                         validators=[DataRequired()])
    colonnes_categories = StringField('Colonnes de catégories', validators=[DataRequired()])
    colonnes_numeriques = StringField('Colonnes numériques', validators=[DataRequired()])
    colonne_sortie = StringField('Colonne de sortie', validators=[DataRequired()])
    sql_query = StringField('Requête SQL', widget=TextArea(), validators=[DataRequired()])
    random_state = IntegerField('Random State', validators=[DataRequired()], default=42)  # Valeur par défaut
    submit = SubmitField('Soumettre')

