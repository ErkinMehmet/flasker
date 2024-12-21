from flask import Blueprint, render_template, request, flash,redirect,url_for,current_app, jsonify
from flasker.app import db
from flasker.models import Users
from flasker.forms import UserForm,LoginForm,ClusteringForm,RegressionForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,current_user,logout_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from flasker.utils.commonFuncs import convert_to_list,sanitize_sql_query
import pickle
from flask import session
import pandas as pd
import json

# Create a Blueprint for user routes
core_bp = Blueprint('core_bp', __name__)

@core_bp.route('/',methods=['GET','POST'])
def index():
    # params pour regression
    from flasker.models import Posts
    posts = Posts.query.order_by(Posts.date_posted.desc()).limit(6).all()
    prediction=0
    predictor=None
    prediction_c=None
    regression_categories=None
    regression_num=None
    pred=None
    pred_c=None
    clustering_form=ClusteringForm()
    regression_form = RegressionForm()
    req = """SELECT pt.paymenttypetitle, amount, TIMESTAMPDIFF(SECOND, p.paymentdate, p.createdat) as secondes, ot.title
                 FROM payment p
                 INNER JOIN payment_type pt ON pt.ID = p.paymenttypeid
                 INNER JOIN organization o ON o.id = p.organizationid
                 INNER JOIN organization_type ot ON ot.id = o.organizationtypeid
                 WHERE paymenttypetitle IN ('Chèque','Virement bancaire')"""
    cols1 = ['paymenttypetitle', 'title']
    cols2 = ['amount']
    cols3 = ['secondes']
    # params pour clustering

    cols1_c = ['autopayment']  # Example value for category columns
    cols2_c = ['operatingbudget', 'days_diff', 'paycount', 'paysum', 'articlecount', 'jobcount', 'coursecount', 'eventcount'] 
    req_c = """select o.ID, 
       o.operatingbudget, 
       o.servedpopulation, 
       ot.title, 
       s.startdate, 
       pt.autopayment,
       COALESCE(p2.paysum, 0) as paysum,
       COALESCE(p2.paycount, 0) as paycount,
       COALESCE(a2.c, 0) as articlecount,
       COALESCE(j2.c, 0) as jobcount,
       COALESCE(c2.c, 0) as coursecount,
       COALESCE(e2.c, 0) as eventcount,
       DATEDIFF(CURDATE(), s.startdate) as days_diff
        from organization o
        inner join organization_type ot
            on ot.id = o.organizationtypeid
        inner join subscription s
            on o.subscriptionid = s.id
        inner join payment_type pt
            on pt.id = s.paymenttypeid
        left join (
            select organizationid, 
                sum(amount) as paysum, 
                count(amount) as paycount 
            from payment p
            group by organizationid
        ) p2
            on p2.organizationid = o.id
        left join (
            select organizationid, 
                count(id) as c 
            from article a
            group by organizationid
        ) a2
            on a2.organizationid = o.id
        left join (
            select organizationid, 
                count(id) as c 
            from job j
            group by organizationid
        ) j2
            on j2.organizationid = o.id
        left join (
            select organizationid, 
                count(id) as c 
            from course c
            group by organizationid
        ) c2
            on c2.organizationid = o.id
        left join (
            select organizationid, 
                count(id) as c 
            from planned_event e
            group by organizationid
        ) e2
            on e2.organizationid = o.id
        where ot.title = 'MRC'
    """
    number_of_clusters=5
    
    def train_predictor_cust(func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            raise RuntimeError(f"An error occurred while executing the function: {str(e)}")

    from flasker.app import create_app
    from flasker.regressors.dt import train_dt_predictor_cust
    from flasker.clustering.kmeanscluster import train_kmeans_c_predictor_cust
    app=current_app
    if request.method=="POST":
        match request.form.get('form_type'):
            case 'regression_form':
                modal=2
                if regression_form.validate_on_submit():
                    match request.form['mesure']:
                        case 'R2':
                            mesure='r2_score'
                    match regression_form.modele.data:
                        case 'Arbre de Décision':
                            func=train_dt_predictor_cust
                        case 'Régression Linéaire':
                            func=train_dt_predictor_cust
                    predictor = train_predictor_cust(func,
                        app,
                        sanitize_sql_query(request.form['sql_query']),
                        0.2,
                        int(request.form['random_state']),
                        convert_to_list(request.form['colonnes_categories']),
                        convert_to_list(request.form['colonnes_numeriques']),
                        convert_to_list(request.form['colonne_sortie']),
                        mesure
                    )
                    print("Voici la mesure du modèle: ",predictor.metric)
                    print("Voici les catégroies:",predictor.categories)
                    print("Voici les champs numériques:",predictor.cols2)
                    prediction=1
                    model_filename = 'predictor.pkl'
                    with open(model_filename, 'wb') as f:
                        pickle.dump(predictor, f)
                    session['model_filename'] = model_filename
                    return render_template("index.html",nom=create_app().config['NAME'],titre=create_app().config['TITLE']
                        ,desc=create_app().config['DESCRIPTION'],clustering_form=clustering_form,
                        regression_form=regression_form,prediction=prediction,categories=predictor.categories,num=predictor.cols2,pred=pred,modal=modal,posts=posts)
            case 'clustering_form':
                modal=1
                if clustering_form.validate_on_submit():
                    match request.form['mesure']:
                        case 'Silhouette':
                            mesure='Silhouette'
                    match clustering_form.modele.data:
                        case 'K-Means':
                            func=train_kmeans_c_predictor_cust
                predictor_c = train_predictor_cust(func,
                        app,
                        sanitize_sql_query(request.form['sql_query']),
                        0.2,
                        int(request.form['random_state']),
                        convert_to_list(request.form['colonnes_categories']),
                        convert_to_list(request.form['colonnes_numeriques']),
                        [],
                        mesure,
                        number_of_clusters
                    )
                model_filename_c = 'predictor_c.pkl'
                with open(model_filename_c, 'wb') as f:
                    pickle.dump(predictor_c, f)
                session['model_filename_c'] = model_filename_c
                print("Voici la mesure du modèle: ",predictor_c.metric)
                print("Voici les catégroies:",predictor_c.categories)
                print("Voici les champs numériques:",predictor_c.cols2)
                return render_template("index.html",nom=create_app().config['NAME'],titre=create_app().config['TITLE']
                    ,desc=create_app().config['DESCRIPTION'],clustering_form=clustering_form,
                    regression_form=regression_form,prediction=prediction_c,categories=predictor_c.categories,num=predictor_c.cols2,pred=pred,modal=modal,posts=posts)
            case 'regression_pred':
                modal=2
                form_data =request.form.to_dict()
                json_data = {"input_data": form_data}

                model_filename = session.get('model_filename')
                if model_filename and os.path.exists(model_filename):
                    with open(model_filename, 'rb') as f:
                        model = pickle.load(f)
                        regression_categories=model.categories
                        print( regression_categories)
                predictor = model
                cols1=model.cols1
                cols2=model.cols2
                input_data = json_data['input_data']
                try:
                    prediction = predictor.predict(input_data)
                    print(prediction)
                    pred= jsonify({"prediction":   {
                            "outcome": prediction.outcome.tolist()[0],
                            "confidence": prediction.confidence,
                            "metric_name":prediction.metric_name
                        }})
                    return render_template("index.html",nom=create_app().config['NAME'],titre=create_app().config['TITLE']
                                ,desc=create_app().config['DESCRIPTION'],clustering_form=clustering_form,
                                regression_form=regression_form,prediction=prediction,categories=predictor.categories,num=predictor.cols2,pred=pred,modal=modal,posts=posts)
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            case 'clustering_pred':
                modal=1
                form_data =request.form.to_dict()
                json_data = {"input_data": form_data}

                model_filename_c = session.get('model_filename_c')
                if model_filename_c and os.path.exists(model_filename_c):
                    with open(model_filename_c, 'rb') as f:
                        model_c = pickle.load(f)
                        clustering_categories=model_c.categories
                predictor_c = model_c
                cols1=model_c.cols1
                cols2=model_c.cols2
                input_data = json_data['input_data']
                print(model_c.categories)
                print(input_data)
                try:
                    prediction_c = predictor_c.predict(input_data)
                    print(model_c.metric_name)
                    pred_c= jsonify({"prediction":   {
                            "outcome": prediction_c.outcome.tolist()[0],
                            "confidence": prediction_c.confidence,
                            "metric_name":prediction_c.metric_name
                        }})
                    print(predictor_c.cols2)
                    return render_template("index.html",nom=create_app().config['NAME'],titre=create_app().config['TITLE']
                                ,desc=create_app().config['DESCRIPTION'],clustering_form=clustering_form,
                                regression_form=regression_form,prediction=prediction_c,categories=predictor_c.categories,num=predictor_c.cols2,pred=pred_c,modal=modal,posts=posts)
                except Exception as e:
                    return jsonify({"error": str(e)}), 500


    # Initialize the form with default values
    regression_form = RegressionForm(
        modele='Arbre de Décision',
        mesure='R2',
        colonnes_categories=','.join(cols1),
        colonnes_numeriques=','.join(cols2),
        colonne_sortie=','.join(cols3),
        sql_query=req,
        random_state=42
    )
    clustering_form = ClusteringForm(
        modele='K-Means',
        mesure='Silhouette',
        colonnes_categories=','.join(cols1_c),  # Convert list to comma-separated string
        colonnes_numeriques=','.join(cols2_c),  # Convert list to comma-separated string
        sql_query=req_c,
        random_state=42,
        number_of_clusters=number_of_clusters
    )
    #print(clustering_form.data)
    return render_template("index.html",nom=create_app().config['NAME'],titre=create_app().config['TITLE']
                           ,desc=create_app().config['DESCRIPTION']
                           ,clustering_form=clustering_form,regression_form=regression_form,prediction=prediction
                           ,categories=regression_categories,num=regression_num,pred=pred,posts=posts)

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
        name_to_update.favorite_color='Bleu'
        name_to_update.about_author=request.form['about_author']
        pic=request.files['profile_pic']
        admin_value = request.form.get('admin')
        if admin_value == 'on':  
            name_to_update.admin = True
        else:
            name_to_update.admin = False

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