from flask import Blueprint, render_template, request, flash
from flasker.app import db
from flasker.models import Users
from flasker.forms import UserForm
from werkzeug.security import generate_password_hash

# Create a Blueprint for user routes
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/add',methods=['GET','POST'])
def add_user():
    name=None
    email=None
    form=UserForm()
    # valider
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # hasher le mdp
            hashed_pw=generate_password_hash(form.password_hash.data)
            user=Users(name=form.name.data,username=form.username.data,email=form.email.data,favorite_color=form.favorite_color.data,password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name=form.name.data
        email=form.email.data
        form.name.data=''
        form.username.data=''
        form.email.data=''
        form.favorite_color.data=''
        form.password_hash.data=''
        form.password_hash2.data=''
        flash("Formulaire soumis avec succès.")
    our_users=Users.query.order_by(Users.createdAt)
    return render_template("add_user.html",name=name,email=email,form=form,our_users=our_users)