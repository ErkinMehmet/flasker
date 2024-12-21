from flask import Blueprint, render_template, request, flash,redirect,url_for,jsonify,current_app
from flasker.app import db
from flasker.models import Posts
from flasker.forms import PostForm,SearchForm
from flask_login import login_required,current_user
import os
from werkzeug.utils import secure_filename

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
    posts_per_page = 5
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    slug_filter = request.args.get('slug', '')
    slugs = Posts.query.with_entities(Posts.slug).distinct()
    query = Posts.query
    if search_query:
        query = query.filter(Posts.title.ilike(f'%{search_query}%'))
    if slug_filter:
        query = query.filter(Posts.slug.ilike(f'%{slug_filter}%')) 
    #posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=posts_per_page, error_out=False)
    #posts=Posts.query.order_by(Posts.date_posted.desc())
    pagination = query.paginate(page=request.args.get('page', 1, type=int), per_page=5)
    return render_template('posts.html',posts=pagination.items, pagination=pagination, slugs=slugs)

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
    

# Check if the file extension is allowed
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    # CKEditor image upload route
    @app.route('/upload-image', methods=['POST'])
    def upload_image():
        if 'upload' not in request.files:
            return jsonify({"error": "No file part"})
        
        file = request.files['upload']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        
        if file and allowed_file(file.filename):
            # Secure the filename and save the image
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Return the URL of the uploaded image
            image_url = url_for('static', filename=f'uploads/{filename}')
            return jsonify({"url": image_url})
        return jsonify({"error": "Invalid file type"})