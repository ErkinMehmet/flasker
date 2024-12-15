from flask import Blueprint, render_template, request, flash
from flasker.app import db
from flasker.models import Users
from flasker.forms import UserForm
from werkzeug.security import generate_password_hash

# Create a Blueprint for user routes
tests = Blueprint('tests', __name__)