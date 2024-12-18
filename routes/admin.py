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
admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin')
@login_required
def admin():
    id=current_user.id
    if id==1:
        return render_template("admin.html")
    else:
        flash("Cette page est réservée pour les admins")
        return redirect(url_for('core_bp.login'))