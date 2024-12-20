from flask import Blueprint, render_template, request, flash,redirect,url_for
from flasker.app import db,admin_required
from flasker.models import Users
from flasker.forms import UserForm,PwdForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,current_user

# Create a Blueprint for user routes
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/add',methods=['GET','POST'])
def add_user():
    name=None
    email=None
    form=UserForm()
    err=''
    # valider
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # hasher le mdp
            hashed_pw=generate_password_hash(form.password_hash.data)
            user=Users(name=form.name.data,username=form.username.data,email=form.email.data,favorite_color='red',about_author=form.about_author.data,password_hash=hashed_pw,admin=form.admin.data)
            db.session.add(user)
            db.session.commit()
            flash("Formulaire soumis avec succès.", "success")
        else:
            err="Le mail existe déjà."
            flash(err, "warning")
            
        name=form.name.data
        email=form.email.data
        form.name.data=''
        form.username.data=''
        form.email.data=''
        form.about_author.data=''
        form.password_hash.data=''
        form.password_hash2.data=''
        
    our_users=Users.query.order_by(Users.createdAt)
    return render_template("add_user.html",name=name,email=email,form=form,our_users=our_users,error=err)

# mettre à jour la bd
@user_bp.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update=Users.query.get_or_404(id)
    our_users=[]
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.username=request.form['username']
        name_to_update.email=request.form['email']
        name_to_update.favorite_color='Bleu'
        name_to_update.about_author=request.form['about_author']
        admin_value = request.form.get('admin')
        if admin_value == 'on':  # 'on' is the default value for checked checkboxes
            name_to_update.admin = True
        else:
            name_to_update.admin = False
            
        try:
            db.session.commit()
            flash("Utilisateur mis à jour avec succès.")
            our_users=Users.query.order_by(Users.createdAt)
            post=1
            if current_user.id==name_to_update.id:
                return redirect(url_for('core_bp.dashboard'))
            elif current_user.admin:
                return redirect(url_for('admin_bp.admin'))
            else:
                return render_template("update.html",form=form,name_to_update=name_to_update,our_users=our_users,p=1)
        except:
            flash("Erreur inattendue.")
            return render_template("update.html",form=form,name_to_update=name_to_update,our_users=our_users,p=2)
    else:
        return render_template("update.html",form=form,name_to_update=name_to_update,our_users=our_users,p=3)

@user_bp.route('/delete/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
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

    

@user_bp.route('/test_pw',methods=['GET','POST'])
@login_required
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