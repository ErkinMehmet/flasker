from flask import Blueprint, render_template, request, flash,redirect,url_for,current_app
from flasker.app import db
from flasker.models import Users
from flasker.forms import UserForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,current_user,logout_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os

# Create a Blueprint for user routes
core_bp = Blueprint('core_bp', __name__)

@core_bp.route('/')
def index():
    moi="Fernando"
    stuff="C'est la m<strong>**de</strong>"
    pizzas=['Pepe','Fromage','Coco',41]
    from flasker.app import create_app
    return render_template("index.html",nom=create_app().config['NAME'],titre=create_app().config['TITLE'],desc=create_app().config['DESCRIPTION'])

# Créer une page d'erreur personalisée
@core_bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@core_bp.errorhandler(500)
def page_not_found(e):
    return render_template("404.html"),500

@core_bp.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@core_bp.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                return redirect(url_for('core_bp.dashboard'))
            else:
                flash("Mdp n'est pas correct.")
        else:
            flash("L'utilisateur n'existe pas.")
    return render_template('login.html',form=form)

@core_bp.route("/dashboard",methods=['GET','POST'])
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
        name_to_update.about_author=request.form['about_author']
        pic=request.files['profile_pic']
        if pic and pic.filename:
            pic_filename=secure_filename(pic.filename)
            pic_name=str(uuid.uuid1(id))+"_"+pic_filename
            name_to_update.profile_pic=pic_name
            upload_folder = current_app.config['UPLOAD_FOLDER']
            pic.save(os.path.join(upload_folder,pic_name))

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

@core_bp.route("/logout",methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("Tu as été bien déconnecté.")
    return redirect(url_for('core_bp.login'))

@core_bp.route("/bubbles",methods=['GET','POST'])
def bubbles():
    return render_template("bubbles.html")

@core_bp.route("/evolution",methods=['GET','POST'])
def evolution():
    return render_template("evolution.html")