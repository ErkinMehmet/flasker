from flask import Blueprint, render_template, request, flash,redirect,url_for
from flasker.app import db
from flasker.models import Posts
from flasker.forms import PostForm,SearchForm
from flask_login import login_required,current_user


# Create a Blueprint for user routes
post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/add-post',methods=['GET','POST'])
# @login_required
def add_post():
    form=PostForm()
    if form.validate_on_submit():
        poster=current_user.id
        post=Posts(title=form.title.data,content=form.content.data,poster_id=poster,slug=form.slug.data)
        form.title.data=''
        form.content.data=''
        form.slug.data=''
        db.session.add(post)
        db.session.commit()
        flash("Poste a été soumis avec succès.")
    return render_template('add_post.html',form=form)

@post_bp.route('/posts',methods=['GET','POST'])
def posts():
    posts=Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html',posts=posts)

@post_bp.route('/posts/<int:id>')
def post(id):
    post=Posts.query.get_or_404(id)
    return render_template('post.html',post=post)

@post_bp.route('/posts/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post=Posts.query.get_or_404(id)
    form=PostForm()
    id=current_user.id
    if form.validate_on_submit():
        post.title=form.title.data
        post.slug=form.slug.data
        post.content=form.content.data
        db.session.add(post)
        db.session.commit()
        flash('Le poste a été modifié!')
        form.title.data=''
        form.slug.data=''
        form.content.data=''
        return redirect(url_for('post_bp.posts'))
    if id==post.poster_id:
        form.title.data=post.title
        form.slug.data=post.slug
        form.content.data=post.content
        return render_template('edit_post.html',form=form)
    else:
        flash('Vous ne pouvez modfiier que vos postes')
        return redirect(url_for('post_bp.posts'))

@post_bp.route('/posts/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete_post(id):
    post=Posts.query.get_or_404(id)
    id=current_user.id
    if id==post.poster_id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Le poste a été supprimé avec succès")
        except:
            flash("Whoops! Il y a eut un problème.")
    else:
        flash('Vous ne pouvez supprimer que vos postes')
    posts=Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html',posts=posts)

@post_bp.route('/search',methods=['POST'])
def search():
    form=SearchForm()
    posts=Posts.query
    if form.validate_on_submit():
        searched=form.searched.data
        posts=posts.filter(Posts.content.like('%'+searched+'%')).order_by(Posts.title).all()
        return render_template("search.html",form=form,searched=searched,posts=posts)