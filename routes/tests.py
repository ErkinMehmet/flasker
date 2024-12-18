from flask import Blueprint, render_template, request, flash
from flasker.forms import NamerForm
from datetime import date
test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/user/<name>')
def user(name):
    #return "<h1>hello {}!</h1>".format(name)
    return render_template("user.html",name=name)

# créer une page de formulaire
@test_bp.route('/name',methods=['GET','POST'])
def name():
    name=None
    form=NamerForm()
    # valider
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash("Formulaire soumis avec succès.")
    return render_template("name.html",name=name,form=form)

@test_bp.route('/date')
def get_curr_date():
    fav={
        "John":"kk",
        "Maria":"funny"
    }
    return {"Date":date.today(),
            "Fav":fav} # dic = json en Python