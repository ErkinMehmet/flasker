from flask import Flask,render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dataclasses import dataclass
from flask_migrate import Migrate
import os
from datetime import date
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.widgets import TextArea
from flask_login import LoginManager,login_required,UserMixin,logout_user,current_user,login_user
from flasker.forms import UserForm,LoginForm,PostForm,PwdForm,NamerForm


@dataclass
class AppEnvironment:
    api_key: str

# initialiser la bd
db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()

from flasker.models import Posts,Users
from flasker.routes.user_routes import user_bp 

def create_app(env: AppEnvironment = None) -> Flask:
    if env is None:
        api_key = os.getenv("API_KEY", "default_api_key")
        env = AppEnvironment(api_key=api_key)

    # créer une instance
    app=Flask(__name__)

    # ajouter la bd SQLite
    #app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # ajouter la bd MySQL
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Fqm123!@localhost/users'#os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    #db=SQLAlchemy(app)
    #migrate=Migrate(app,db)

    @app.route('/date')
    def get_curr_date():
        fav={
            "John":"kk",
            "Maria":"funny"
        }
        return {"Date":date.today(),
                "Fav":fav} # dic = json en Python

    # Flask login
    login_manager.init_app(app)
    login_manager.login_view='login'
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    app.register_blueprint(user_bp)

    # créer une décorateur de route
    @app.route('/')
    #def index():
        #return "<h1>hello world!</h1>"
    def index():
        moi="Fernando"
        flash("Bienvenue au site de Fernando2")
        stuff="C'est la m<strong>**de</strong>"
        pizzas=['Pepe','Fromage','Coco',41]
        return render_template("index.html",nom=moi,contenu=stuff,pizzas=pizzas)

    # localhost:5000/user/john
    @app.route('/user/<name>')
    def user(name):
        #return "<h1>hello {}!</h1>".format(name)
        return render_template("user.html",name=name)


    # Créer une page d'erreur personalisée
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"),404

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template("404.html"),500

    # créer une page de formulaire
    @app.route('/name',methods=['GET','POST'])
    def name():
        name=None
        form=NamerForm()
        # valider
        if form.validate_on_submit():
            name=form.name.data
            form.name.data=''
            flash("Formulaire soumis avec succès.")

        return render_template("name.html",name=name,form=form)

    # mettre à jour la bd
    @app.route('/update/<int:id>',methods=['GET','POST'])
    @login_required
    def update(id):
        form = UserForm()
        name_to_update=Users.query.get_or_404(id)
        our_users=[]
        if request.method=="POST":
            name_to_update.name=request.form['name']
            name_to_update.username=request.form['username']
            name_to_update.email=request.form['email']
            name_to_update.favorite_color=request.form['favorite_color']
            try:
                db.session.commit()
                flash("Utilisateur mis à jour avec succès.")
                our_users=Users.query.order_by(Users.createdAt)
                post=1
                return render_template("update.html",form=form,name_to_update=name_to_update,our_users=our_users,p=1)
            except:
                flash("Erreur inattendue.")
                return render_template("update.html",form=form,name_to_update=name_to_update,our_users=our_users,p=2)
        else:
            return render_template("update.html",form=form,name_to_update=name_to_update,our_users=our_users,p=3)
    
    @app.route('/delete/<int:id>',methods=['GET','POST'])
    def delete(id):
        name=None
        form=UserForm()
        user_to_delete=Users.query.get_or_404(id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("L'utilisateur a été supprimé avec succès")
            our_users=Users.query.order_by(Users.createdAt)
            return render_template("add_user.html",name=name,form=form,our_users=our_users)
        except:
            flash("Whoops il y eut un problème!")
            return render_template("add_user.html",name=name,form=form,our_users=our_users)

    @app.route('/test_pw',methods=['GET','POST'])
    def test_pw():
        email=None
        pwd=None
        pwd2=None
        ok=None
        form=PwdForm()
        # valider
        if form.validate_on_submit():
            email=form.email.data
            pwd=form.password_hash.data
            form.email.data=''
            form.password_hash=''
            pwd2=Users.query.filter_by(email=email).first()
            ok=check_password_hash(pwd2.password_hash,pwd)

            flash("Formulaire soumis avec succès.")

        return render_template("test_pw.html",email=email,pwd=pwd,pwd2=pwd2,form=form,ok=ok)
    
    @app.route('/add-post',methods=['GET','POST'])
    # @login_required
    def add_post():
        form=PostForm()


        if form.validate_on_submit():
            post=Posts(title=form.title.data,content=form.content.data,author=form.author.data,slug=form.slug.data)
            form.title.data=''
            form.content.data=''
            form.slug.data=''
            form.author.data=''
            db.session.add(post)
            db.session.commit()
            flash("Poste a été soumis avec succès.")
        return render_template('add_post.html',form=form)

    @app.route('/posts',methods=['GET','POST'])
    def posts():
        posts=Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',posts=posts)
    
    @app.route('/posts/<int:id>')
    def post(id):
        post=Posts.query.get_or_404(id)
        return render_template('post.html',post=post)
    
    @app.route('/posts/edit/<int:id>',methods=['GET','POST'])
    @login_required
    def edit_post(id):
        post=Posts.query.get_or_404(id)
        form=PostForm()
        if form.validate_on_submit():
            post.title=form.title.data
            post.author=form.author.data
            post.slug=form.slug.data
            post.content=form.content.data
            db.session.add(post)
            db.session.commit()
            flash('Le poste a été modifié!')
            form.title.data=''
            form.author.data=''
            form.slug.data=''
            form.content.data=''
            return redirect(url_for('post',id=post.id))
        form.title.data=post.title
        form.author.data=post.author
        form.slug.data=post.slug
        form.content.data=post.content
        return render_template('edit_post.html',form=form)

    @app.route('/posts/delete/<int:id>',methods=['GET','POST'])
    @login_required
    def delete_post(id):
        post=Posts.query.get_or_404(id)
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Le poste a été supprimé avec succès")
        except:
            flash("Whoops! Il y a eut un problème.")
        posts=Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',posts=posts)
    
    @app.route("/login",methods=['GET','POST'])
    def login():
        form=LoginForm()
        if form.validate_on_submit():
            user=Users.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password_hash,form.password.data):
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    flash("Mdp n'est pas correct.")
            else:
                flash("L'utilisateur n'existe pas.")
        return render_template('login.html',form=form)

    @app.route("/dashboard",methods=['GET','POST'])
    @login_required
    def dashboard():
        form = UserForm()
        id=current_user.id
        name_to_update=Users.query.get_or_404(id)
        our_users=[]
        if request.method=="POST":
            name_to_update.name=request.form['name']
            name_to_update.username=request.form['username']
            name_to_update.email=request.form['email']
            name_to_update.favorite_color=request.form['favorite_color']
            try:
                db.session.commit()
                flash("Utilisateur mis à jour avec succès.")
                our_users=Users.query.order_by(Users.createdAt)
                post=1
                return render_template("dashboard.html",form=form,name_to_update=name_to_update,our_users=our_users,p=1)
            except:
                flash("Erreur inattendue.")
                return render_template("dashboard.html",form=form,name_to_update=name_to_update,our_users=our_users,p=2)
        else:
            return render_template("dashboard.html",form=form,name_to_update=name_to_update,our_users=our_users,p=3)
    
    @app.route("/logout",methods=['GET','POST'])
    @login_required
    def logout():
        logout_user()
        flash("Tu as été bien déconnecté.")
        return redirect(url_for('login'))

    return app